from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Course
from sqlalchemy import or_

courses_bp = Blueprint('courses', __name__)


@courses_bp.route('/courses')
def list_courses():
    q = request.args.get('q', '').strip()
    if q:
        search = f'%{q}%'
        courses = Course.query.filter(
            or_(
                Course.course_code.ilike(search),
                Course.name.ilike(search),
                Course.category.ilike(search),
                Course.description.ilike(search),
            )
        ).order_by(Course.name).all()
    else:
        courses = Course.query.order_by(Course.name).all()
    return render_template('courses/list.html', courses=courses, q=q)


@courses_bp.route('/courses/create', methods=['GET', 'POST'])
@login_required
def create_course():
    if request.method == 'POST':
        course_code = request.form.get('course_code', '').strip()
        name = request.form.get('name', '').strip()
        credits = request.form.get('credits', '3').strip()
        category = request.form.get('category', '').strip()
        is_required = request.form.get('is_required') == 'on'
        description = request.form.get('description', '').strip()

        if not course_code or not name:
            flash('Mã học phần và tên là bắt buộc.', 'danger')
            return render_template('courses/form.html', course=None)

        if Course.query.filter_by(course_code=course_code).first():
            flash('Mã học phần đã tồn tại.', 'danger')
            return render_template('courses/form.html', course=None)

        try:
            credits = int(credits)
        except ValueError:
            flash('Số tín chỉ phải là số nguyên.', 'danger')
            return render_template('courses/form.html', course=None)

        course = Course(
            course_code=course_code, name=name, credits=credits,
            category=category, is_required=is_required, description=description
        )
        db.session.add(course)
        db.session.commit()
        flash('Tạo học phần thành công!', 'success')
        return redirect(url_for('courses.list_courses'))

    return render_template('courses/form.html', course=None)


@courses_bp.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)

    if request.method == 'POST':
        course_code = request.form.get('course_code', '').strip()
        name = request.form.get('name', '').strip()
        credits = request.form.get('credits', '3').strip()
        category = request.form.get('category', '').strip()
        is_required = request.form.get('is_required') == 'on'
        description = request.form.get('description', '').strip()

        if not course_code or not name:
            flash('Mã học phần và tên là bắt buộc.', 'danger')
            return render_template('courses/form.html', course=course)

        existing = Course.query.filter(
            Course.course_code == course_code,
            Course.id != course.id
        ).first()
        if existing:
            flash('Mã học phần đã tồn tại.', 'danger')
            return render_template('courses/form.html', course=course)

        try:
            credits = int(credits)
        except ValueError:
            flash('Số tín chỉ phải là số nguyên.', 'danger')
            return render_template('courses/form.html', course=course)

        course.course_code = course_code
        course.name = name
        course.credits = credits
        course.category = category
        course.is_required = is_required
        course.description = description
        db.session.commit()
        flash('Cập nhật học phần thành công!', 'success')
        return redirect(url_for('courses.list_courses'))

    return render_template('courses/form.html', course=course)


@courses_bp.route('/courses/<int:course_id>')
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    program_courses = (
        Course.query.filter_by(id=course_id)
        .first()
        .program_courses
    )
    return render_template('courses/detail.html', course=course, program_courses=program_courses)


@courses_bp.route('/courses/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash('Xóa học phần thành công!', 'success')
    return redirect(url_for('courses.list_courses'))
