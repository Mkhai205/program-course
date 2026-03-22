import time
from app import create_app, db
from app.models import User, Program, Course, ProgramCourse


def wait_for_db(app, max_retries=30, delay=2):
    """Wait for the database to be ready."""
    for i in range(max_retries):
        try:
            with app.app_context():
                db.engine.connect()
            return True
        except Exception:
            print(f"Waiting for database... ({i + 1}/{max_retries})")
            time.sleep(delay)
    return False


def seed_data():
    """Seed initial data if tables are empty."""
    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', is_admin=True)
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created (username: admin, password: admin123)")

    if Program.query.first() is not None:
        return

    # Sample programs
    programs = [
        Program(program_code='CNTT01', name='Công nghệ thông tin',
                description='Chương trình đào tạo ngành Công nghệ thông tin'),
        Program(program_code='KTPM01', name='Kỹ thuật phần mềm',
                description='Chương trình đào tạo ngành Kỹ thuật phần mềm'),
        Program(program_code='HTTT01', name='Hệ thống thông tin',
                description='Chương trình đào tạo ngành Hệ thống thông tin'),
    ]

    # Sample courses
    courses = [
        Course(course_code='MAT101', name='Toán cao cấp 1', credits=3, category='Đại cương', is_required=True,
               description='Cung cấp kiến thức nền tảng về giải tích và đại số tuyến tính. Học sinh sẽ học về hàm số, giới hạn, đạo hàm, tích phân và các ứng dụng của chúng.'),
        Course(course_code='MAT102', name='Toán cao cấp 2', credits=3, category='Đại cương', is_required=True,
               description='Tiếp tục phát triển các kiến thức toán học cao cấp. Bao gồm phương trình vi phân, chuỗi số, chứng minh logic toán học và các ứng dụng thực tiễn.'),
        Course(course_code='PHY101', name='Vật lý đại cương', credits=3, category='Đại cương', is_required=True,
               description='Giới thiệu các khái niệm cơ bản về vật lý. Bao gồm cơ học, nhiệt học, điện từ học và quang học. Cung cấp nền tảng khoa học cho các ngành kỹ thuật.'),
        Course(course_code='CS101', name='Nhập môn lập trình', credits=3, category='Cơ sở ngành', is_required=True,
               description='Khóa học nhập môn lập trình cho người mới bắt đầu. Học các khái niệm cơ bản: biến, kiểu dữ liệu, điều kiện, vòng lặp, hàm. Sử dụng ngôn ngữ Python.'),
        Course(course_code='CS102', name='Cấu trúc dữ liệu và giải thuật', credits=4, category='Cơ sở ngành', is_required=True,
               description='Nghiên cứu các cấu trúc dữ liệu phổ biến (mảng, danh sách, cây, đồ thị) và các giải thuật tối ưu. Phân tích độ phức tạp thời gian và không gian.'),
        Course(course_code='CS201', name='Cơ sở dữ liệu', credits=3, category='Cơ sở ngành', is_required=True,
               description='Thiết kế và quản lý cơ sở dữ liệu quan hệ. Học SQL, mô hình dữ liệu, bình thường hóa, truy vấn và tối ưu hóa cơ sở dữ liệu.'),
        Course(course_code='CS202', name='Mạng máy tính', credits=3, category='Cơ sở ngành', is_required=True,
               description='Giới thiệu các nguyên lý mạng máy tính. Bao gồm mô hình OSI, TCP/IP, định tuyến, giao thức truyền thông và bảo mật mạng.'),
        Course(course_code='CS301', name='Hệ điều hành', credits=3, category='Chuyên ngành', is_required=True,
               description='Tìm hiểu các chức năng chính của hệ điều hành: quản lý tiến trình, bộ nhớ, I/O và hệ thống tập tin. Nghiên cứu các hệ điều hành phổ biến.'),
        Course(course_code='SE301', name='Công nghệ phần mềm', credits=3, category='Chuyên ngành', is_required=True,
               description='Các phương pháp, quy trình và công cụ phát triển phần mềm. Bao gồm thiết kế phần mềm, mô hình hóa UML, kiểm thử và bảo trì phần mềm.'),
        Course(course_code='SE302', name='Kiểm thử phần mềm', credits=3, category='Chuyên ngành', is_required=False,
               description='Các kỹ thuật kiểm thử phần mềm chi tiết. Học về kiểm thử hộp đen/trắng, kiểm thử tự động, phát hiện lỗi và quản lý chất lượng phần mềm.'),
        Course(course_code='AI301', name='Trí tuệ nhân tạo', credits=3, category='Chuyên ngành', is_required=False,
               description='Giới thiệu các khái niệm trí tuệ nhân tạo, học máy và xử lý ngôn ngữ tự nhiên. Bao gồm các thuật toán tìm kiếm, mạng nơ-ron và ứng dụng AI.'),
        Course(course_code='WEB301', name='Phát triển ứng dụng Web', credits=3, category='Chuyên ngành', is_required=False,
               description='Phát triển các ứng dụng web hiện đại. Học HTML, CSS, JavaScript, frameworkweb, phát triển phía servidor và client, và triển khai ứng dụng web.'),
    ]

    for p in programs:
        db.session.add(p)
    for c in courses:
        db.session.add(c)
    db.session.flush()

    # Assign courses to CNTT program
    cntt = programs[0]
    assignments = [
        (courses[0], 1, 1), (courses[2], 1, 2), (courses[3], 1, 3),
        (courses[1], 2, 1), (courses[4], 2, 2),
        (courses[5], 3, 1), (courses[6], 3, 2),
        (courses[7], 4, 1), (courses[8], 4, 2),
        (courses[10], 5, 1), (courses[11], 5, 2),
    ]
    for course, semester, sort_order in assignments:
        db.session.add(ProgramCourse(
            program_id=cntt.id, course_id=course.id,
            semester=semester, sort_order=sort_order
        ))

    db.session.commit()
    print("Seed data created successfully!")


app = create_app()

if __name__ == '__main__':
    wait_for_db(app)
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(host='0.0.0.0', port=5000, debug=True)
