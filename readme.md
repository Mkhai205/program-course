code python flask sqlalchemy (postgres database docker compose)

Hãy xây dựng cơ sở dữ liệu gồm các bảng lưu trữ thông tin như trên

Hãy xây dựng giao diện cho phép tìm kiếm (1 ô text search) và cho phép tự tìm kiếm theo các trường thông tin trên và hiển thị danh sách các Chương trình phù hợp với tiêu chí tìm kiếm

Hãy xây dựng chức năng quản trị cho phép một người dùng Admin có quyền quản lý danh sách Chương trình như trên.

Hãy xây dựng chức năng quản lý thông tin các Học phần toàn trường

Quản lý chọn các môn học từ một danh sách Học phần toàn trường vào chương trình này và lựa chọn số thứ tự xuất hiện cũng như học kỳ sẽ học

Xây dựng chức năng hiển thị chi tiết các Học phần học theo chương trình theo bảng trên

## Programs

id (PK)
program_code
name
description

## Courses

id (PK)
course_code
name
credits
category
is_required
description

## Program_Courses

id (PK)
program_id (FK)
course_id (FK)
semester
