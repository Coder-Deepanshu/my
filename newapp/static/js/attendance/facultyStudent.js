

$(document).ready(function() {
        // CSRF token handling
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                }
            }
        });

        // Auto-dismiss alerts after 5 seconds
        setTimeout(() => {
            $('.alert').alert('close');
        }, 5000);

        // Course change handler
        $('#course').change(function() {
            const course = $(this).val();
            console.log('Course changed:', course);
            
            if (course !== 'all') {
                $.get('{% url "getCourseDetails" %}', {course_name: course}, function(data) {
                    console.log('Course details response:', data);
                    
                    if (data.error) {
                        showMessage(data.error, 'danger');
                        return;
                    }
                    
                    // Update year and semester dropdowns
                    $('#year').empty().append('<option value="all">All Years</option>');
                    $('#semester').empty().append('<option value="all">All Semesters</option>');
                    
                    // Populate years
                    if (data.years && data.years.length > 0) {
                        data.years.forEach(year => {
                            $('#year').append(`<option value="${year}">Year ${year}</option>`);
                        });
                    }
                    
                    // Populate semesters
                    if (data.semesters && data.semesters.length > 0) {
                        data.semesters.forEach(sem => {
                            $('#semester').append(`<option value="${sem}">Semester ${sem}</option>`);
                        });
                    }

                    // Update lecture dropdown
                    $('#lecture').empty().append('<option value="">Select Lecture</option>');
                    if (data.lectures && data.lectures.length > 0) {
                        data.lectures.forEach(lecture => {
                            $('#lecture').append(`<option value="${lecture}">Lecture ${lecture}</option>`);
                        });
                    }
                    
                    $('#year, #semester, #lecture').prop('disabled', false);
                }).fail(function(xhr) {
                    console.error('AJAX error:', xhr);
                    let errorMsg = 'Failed to load course details';
                    try {
                        const response = JSON.parse(xhr.responseText);
                        errorMsg = response.error || errorMsg;
                    } catch (e) {
                        errorMsg = 'Server error occurred';
                    }
                    showMessage(errorMsg, 'danger');
                });
            } else {
                $('#year, #semester, #lecture').prop('disabled', true);
            }
        });

        // Filter students function
        function filterStudents() {
            const filters = {
                course: $('#course').val(),
                year: $('#year').val(),
                semester: $('#semester').val(),
                college_id: $('#college_id').val()
            };

            console.log('Applying filters:', filters);

            $('#loading').show();
            $('#results').html('');
            $('#attendanceControls').hide();
            
            $.get('{% url "filteredStudents" %}', filters, function(data) {
                $('#results').html(data.html);
                $('#attendanceControls').show();
            }).fail(function(xhr) {
                console.error('Filter error:', xhr);
                showMessage('Failed to load student data. Please try again.', 'danger');
            }).always(function() {
                $('#loading').hide();
            });
        }

            // Save attendance function
            $('#save-attendance').click(function() {
                const lecture = $('#lecture').val();
                const date = $('#attendance-date').val();
                const course = $('#course').val();
                
                if (!lecture) {
                    showMessage('Please select a lecture number', 'danger');
                    return;
                }
                
                if (!date) {
                    showMessage('Please select a date', 'danger');
                    return;
                }
                
                if (!course || course === 'all') {
                    showMessage('Please select a specific course', 'danger');
                    return;
                }
                
                const attendanceData = [];
                $('.attendance-status').each(function() {
                    const studentId = $(this).data('student-id');
                    const status = $(this).val();
                    
                    if (status) {
                        attendanceData.push({
                            student_id: studentId,
                            status: status
                        });
                    }
                });
                
                if (attendanceData.length === 0) {
                    showMessage('No attendance data to save', 'danger');
                    return;
                }
                
                $('#save-attendance').prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Saving...');
                
                $.ajax({
                    url: '/save_attendance/',
                    method: 'POST',
                    data: {
                        lecture: lecture,
                        date: date,
                        course: course,
                        attendance: JSON.stringify(attendanceData),
                        csrfmiddlewaretoken: '{{ csrf_token }}'
                    },
                    success: function(response) {
                        if (response.success) {
                            let message = response.message;
                            
                            // Show warning if duplicates found
                            if (response.duplicate_entries && response.duplicate_entries.length > 0) {
                                const names = response.duplicate_entries.map(s => s.student_name).join(', ');
                                message += `<br><strong>Warning:</strong> Attendance already exists for ${names}`;
                                
                                // Highlight duplicate entries in the table
                                response.duplicate_entries.forEach(entry => {
                                    $(`.attendance-status[data-student-id="${entry.student_id}"]`)
                                        .closest('tr')
                                        .css('background-color', '#fff3cd');
                                });
                            }
                            
                            showMessage(message, 'success');
                        } else {
                            showMessage(response.error || 'Failed to save attendance', 'danger');
                        }
                    },
                    error: function(xhr) {
                        let errorMsg = 'Failed to save attendance';
                        try {
                            const response = JSON.parse(xhr.responseText);
                            errorMsg = response.error || errorMsg;
                        } catch (e) {}
                        showMessage(errorMsg, 'danger');
                    },
                    complete: function() {
                        $('#save-attendance').prop('disabled', false).html('<i class="fas fa-save"></i> Save Attendance');
                    }
                });
            });

            // Show message function
            function showMessage(message, type) {
                const alertClass = type === 'success' ? 'alert-success' : 
                                  type === 'warning' ? 'alert-warning' : 'alert-danger';
                const alertHtml = `
                    <div class="alert ${alertClass} alert-dismissible fade show">
                        <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
                        ${message}
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>
                `;
                
                // Remove existing alerts
                $('.alert-dismissible').remove();
                
                // Add new alert
                $('.page-header').after(alertHtml);
                
                // Auto dismiss after 5 seconds
                setTimeout(() => {
                    $('.alert').alert('close');
                }, 5000);
            }

            $('#filterBtn').click(filterStudents);
        
        $('#college_id').keypress(function(e) {
            if (e.which === 13) {
                filterStudents();
            }
        });
    });