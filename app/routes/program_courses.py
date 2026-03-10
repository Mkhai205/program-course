from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Program, Course, ProgramCourse

program_courses_bp = Blueprint('program_courses', __name__)


@program_courses_bp.route('/programs/<int:program_id>/courses', methods=['GET', 'POST'])
@login_required
def manage(program_id):
    program = Program.query.get_or_404(program_id)

    if request.method == 'POST':
        course_id = request.form.get('course_id', type=int)
        semester = request.form.get('semester', type=int)
        sort_order = request.form.get('sort_order', 0, type=int)

        if not course_id or not semester:
            flash('Vui lòng chọn học phần và nhập học kỳ.', 'danger')
            return redirect(url_for('program_courses.manage', program_id=program_id))

        existing = ProgramCourse.query.filter_by(
            program_id=program_id, course_id=course_id
        ).first()
        if existing:
            flash('Học phần đã có trong chương trình này.', 'warning')
            return redirect(url_for('program_courses.manage', program_id=program_id))

        pc = ProgramCourse(
            program_id=program_id, course_id=course_id,
            semester=semester, sort_order=sort_order
        )
        db.session.add(pc)
        db.session.commit()
        flash('Thêm học phần vào chương trình thành công!', 'success')
        return redirect(url_for('program_courses.manage', program_id=program_id))

    program_courses = (
        ProgramCourse.query
        .filter_by(program_id=program_id)
        .order_by(ProgramCourse.semester, ProgramCourse.sort_order)
        .all()
    )

    assigned_ids = [pc.course_id for pc in program_courses]
    available_courses = Course.query.filter(
        ~Course.id.in_(assigned_ids) if assigned_ids else True
    ).order_by(Course.name).all()

    return render_template(
        'program_courses/manage.html',
        program=program,
        program_courses=program_courses,
        available_courses=available_courses,
    )


@program_courses_bp.route('/programs/<int:program_id>/courses/<int:pc_id>/edit', methods=['POST'])
@login_required
def edit(program_id, pc_id):
    pc = ProgramCourse.query.get_or_404(pc_id)
    semester = request.form.get('semester', type=int)
    sort_order = request.form.get('sort_order', 0, type=int)

    if semester:
        pc.semester = semester
    pc.sort_order = sort_order
    db.session.commit()
    flash('Cập nhật thành công!', 'success')
    return redirect(url_for('program_courses.manage', program_id=program_id))


@program_courses_bp.route('/programs/<int:program_id>/courses/<int:pc_id>/delete', methods=['POST'])
@login_required
def remove(program_id, pc_id):
    pc = ProgramCourse.query.get_or_404(pc_id)
    db.session.delete(pc)
    db.session.commit()
    flash('Xóa học phần khỏi chương trình thành công!', 'success')
    return redirect(url_for('program_courses.manage', program_id=program_id))
