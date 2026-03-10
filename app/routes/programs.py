from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app import db
from app.models import Program, ProgramCourse
from sqlalchemy import or_

programs_bp = Blueprint('programs', __name__)


@programs_bp.route('/')
def index():
    q = request.args.get('q', '').strip()
    if q:
        search = f'%{q}%'
        programs = Program.query.filter(
            or_(
                Program.program_code.ilike(search),
                Program.name.ilike(search),
                Program.description.ilike(search),
            )
        ).order_by(Program.name).all()
    else:
        programs = Program.query.order_by(Program.name).all()
    return render_template('programs/list.html', programs=programs, q=q)


@programs_bp.route('/programs/create', methods=['GET', 'POST'])
@login_required
def create_program():
    if request.method == 'POST':
        program_code = request.form.get('program_code', '').strip()
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not program_code or not name:
            flash('Mã chương trình và tên là bắt buộc.', 'danger')
            return render_template('programs/form.html', program=None)

        if Program.query.filter_by(program_code=program_code).first():
            flash('Mã chương trình đã tồn tại.', 'danger')
            return render_template('programs/form.html', program=None)

        program = Program(program_code=program_code, name=name, description=description)
        db.session.add(program)
        db.session.commit()
        flash('Tạo chương trình thành công!', 'success')
        return redirect(url_for('programs.index'))

    return render_template('programs/form.html', program=None)


@programs_bp.route('/programs/<int:program_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_program(program_id):
    program = Program.query.get_or_404(program_id)

    if request.method == 'POST':
        program_code = request.form.get('program_code', '').strip()
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()

        if not program_code or not name:
            flash('Mã chương trình và tên là bắt buộc.', 'danger')
            return render_template('programs/form.html', program=program)

        existing = Program.query.filter(
            Program.program_code == program_code,
            Program.id != program.id
        ).first()
        if existing:
            flash('Mã chương trình đã tồn tại.', 'danger')
            return render_template('programs/form.html', program=program)

        program.program_code = program_code
        program.name = name
        program.description = description
        db.session.commit()
        flash('Cập nhật chương trình thành công!', 'success')
        return redirect(url_for('programs.index'))

    return render_template('programs/form.html', program=program)


@programs_bp.route('/programs/<int:program_id>/delete', methods=['POST'])
@login_required
def delete_program(program_id):
    program = Program.query.get_or_404(program_id)
    db.session.delete(program)
    db.session.commit()
    flash('Xóa chương trình thành công!', 'success')
    return redirect(url_for('programs.index'))


@programs_bp.route('/programs/<int:program_id>')
def program_detail(program_id):
    program = Program.query.get_or_404(program_id)
    program_courses = (
        ProgramCourse.query
        .filter_by(program_id=program_id)
        .order_by(ProgramCourse.semester, ProgramCourse.sort_order)
        .all()
    )

    semesters = {}
    for pc in program_courses:
        semesters.setdefault(pc.semester, []).append(pc)

    return render_template('programs/detail.html', program=program, semesters=semesters)
