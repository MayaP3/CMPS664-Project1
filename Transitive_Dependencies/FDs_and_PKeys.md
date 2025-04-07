# Student_Course_Registration
# FDs: StudentID|CourseID -> StudentName, CourseName, InstructorName, InstructorPhone; CourseID -> CourseName, InstructorName, InstructorPhone
# PKeys: StudentID, CourseID

# Employee Department 
# FDs: EmployeeID -> EmployeeName, DepartmentID, DepartmentName, DepartmentManager, ManagerEmail; DepartmentID -> DepartmentName, DepartmentManager, ManagerEmail
# PKeys: EmployeeID

# Orders and Products
# FDs: OrderID|ProductID -> OrderDate, ProductName, ProductPrice, CustomerName; ProductID -> ProductName, ProductPrice
# PKeys: OrderID, ProductID