from flask import *
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import *


app=Flask(__name__,static_url_path='/static')
app.secret_key = "4db8ghfhb51a4017e427f3ea5c2137c450f767dce1bf"  

app.config['MYSQL_HOST'] = 'localhost'#hostname
app.config['MYSQL_USER'] = 'root'#username

app.config['MYSQL_PASSWORD'] = '1234'#password G@nesh24


app.config['MYSQL_DB'] = 'hrms'#database name

mysql = MySQL(app)



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/signup")
def signup():
    return render_template('signup.html')

@app.route("/home")
def rehome():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Employee WHERE EmployeeID = % s', (session['id'],))
    emp=cursor.fetchone()
    cursor.execute('select * from EmployeeEducation ee join Education e  where ee.EducationID=e.EducationID and ee.EmployeeID = % s', (session['id'],))
    education=cursor.fetchall()
    cursor.execute('SELECT * FROM EmployeeProject e join Project p where e.projectid=p.projectid and EmployeeID = % s', (session['id'],))
    project=cursor.fetchall()
    cursor.execute('select * from EmployeeSkill e join Skill s where e.skillid=s.skillid and EmployeeID = % s', (session['id'],))
    skill=cursor.fetchall()
    cursor.execute('select * from EmployeeCertification e join  Certification c where e.CertificationID=c.CertificationID and  EmployeeID = % s', (session['id'],))
    certification=cursor.fetchall()
    cursor.execute('SELECT t.TrainingName, t.TrainingDescription,et.TrainingDate FROM Training t JOIN EmployeeTraining et ON t.TrainingID = et.TrainingID JOIN Employee e ON et.EmployeeID = e.EmployeeID where  e.EmployeeID = % s', (session['id'],))
    training=cursor.fetchall()
    return render_template('home.html',emp=emp,education=education,project=project,skill=skill,certification=certification,training=training)

@app.route("/adminhome")
def adminhome():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Employee')
    emp=cursor.fetchall()
    cursor.execute('select * from Education')
    education=cursor.fetchall()
    cursor.execute('SELECT * FROM project')
    project=cursor.fetchall()
    cursor.execute('select * from Skill')
    skill=cursor.fetchall()
    cursor.execute('select * from Certification')
    certification=cursor.fetchall()
    cursor.execute('SELECT * from training')
    training=cursor.fetchall()
    cursor.execute('SELECT COUNT(*) AS total_employees,(SELECT COUNT(*) FROM Skill) AS total_skills,(SELECT COUNT(*) FROM Project) AS total_projects,(SELECT COUNT(*) FROM Certification) AS total_certifications,(SELECT COUNT(*) FROM Training) AS total_trainings,(SELECT COUNT(*) FROM Report) AS total_reports FROM Employee')
    count=cursor.fetchone()
    return render_template('adminhome.html',admin=admin,emp=emp,education=education,project=project,skill=skill,certification=certification,training=training,count=count)
    
@app.route("/sign", methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        name = request.form['name']
        experience = request.form['experience']
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Employee (Name, Experience, LoginID, Password) VALUES (%s, %s, %s, %s)', (name,experience,email, password))
        mysql.connection.commit()
        return redirect("/")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Employee WHERE LoginID = % s AND password = % s', (email, password))
        account = cursor.fetchone()
        if account:
            session['id'] = account['EmployeeID']
            session['email'] = account['LoginID']
            cursor.execute('SELECT * FROM Employee WHERE LoginID = % s', (email,))
            emp=cursor.fetchone()
            cursor.execute('select * from EmployeeEducation ee join Education e  where ee.EducationID=e.EducationID and ee.EmployeeID = % s', (account['EmployeeID'],))
            education=cursor.fetchall()
            cursor.execute('SELECT * FROM EmployeeProject e join Project p where e.projectid=p.projectid and EmployeeID = % s', (account['EmployeeID'],))
            project=cursor.fetchall()
            cursor.execute('select * from EmployeeSkill e join Skill s where e.skillid=s.skillid and EmployeeID = % s', (account['EmployeeID'],))
            skill=cursor.fetchall()
            cursor.execute('select * from EmployeeCertification e join  Certification c where e.CertificationID=c.CertificationID and  EmployeeID = % s', (account['EmployeeID'],))
            certification=cursor.fetchall()
            cursor.execute('SELECT t.TrainingName, t.TrainingDescription,et.TrainingDate FROM Training t JOIN EmployeeTraining et ON t.TrainingID = et.TrainingID JOIN Employee e ON et.EmployeeID = e.EmployeeID where  e.EmployeeID = % s', (account['EmployeeID'],))
            training=cursor.fetchall()
            return render_template('home.html',emp=emp,education=education,project=project,skill=skill,certification=certification,training=training)
        else:
            flash("Not Login")
                
@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/education")
def education():
    return render_template('education.html')

@app.route('/addempeducation/<int:id>', methods=['GET', 'POST'])
def addempeducation(id):
    if request.method == 'POST':
        degree = request.form['degree']
        university = request.form['university']
        yearofgraduation = request.form['yearofgraduation']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Education (DegreeName, University, YearOfGraduation)  VALUES (%s, %s, %s)', (degree,university,yearofgraduation))
        mysql.connection.commit()
        educationid = cursor.lastrowid
        cursor.execute('INSERT INTO EmployeeEducation (EmployeeID, EducationID)  VALUES (%s, %s)', (id,educationid))
        mysql.connection.commit()
        return redirect('/home')

@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM administration where AdminEmail=%s and AdminPassword=%s',(email,password))
        admin = cursor.fetchone()
        if admin:
            session['id'] = admin['AdminID']
            session['email'] = admin['AdminEmail']
            cursor.execute('SELECT * FROM Employee')
            emp=cursor.fetchall()
            cursor.execute('select * from Education')
            education=cursor.fetchall()
            cursor.execute('SELECT * FROM project')
            project=cursor.fetchall()
            cursor.execute('select * from Skill')
            skill=cursor.fetchall()
            cursor.execute('select * from Certification')
            certification=cursor.fetchall()
            cursor.execute('SELECT * from Training')
            training=cursor.fetchall()
            cursor.execute('SELECT COUNT(*) AS total_employees,(SELECT COUNT(*) FROM Skill) AS total_skills,(SELECT COUNT(*) FROM Project) AS total_projects,(SELECT COUNT(*) FROM Certification) AS total_certifications,(SELECT COUNT(*) FROM Training) AS total_trainings,(SELECT COUNT(*) FROM Report) AS total_reports FROM Employee')
            count=cursor.fetchone()
            return render_template('adminhome.html',admin=admin,emp=emp,education=education,project=project,skill=skill,certification=certification,training=training,count=count)
    
        
@app.route('/empdetails/<int:id>')
def empdetils(id):
    if id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM employee WHERE EmployeeID = % s', (id,))
        account = cursor.fetchone()
        if account:
            cursor.execute('SELECT * FROM Employee WHERE EmployeeID = % s', (id,))
            emp=cursor.fetchone()
            cursor.execute('select * from EmployeeEducation ee join Education e  where ee.EducationID=e.EducationID and ee.EmployeeID = % s', (id,))
            education=cursor.fetchall()
            cursor.execute('SELECT * FROM EmployeeProject e join Project p where e.projectid=p.projectid and EmployeeID = % s', (id,))
            project=cursor.fetchall()
            cursor.execute('select * from EmployeeSkill e join Skill s where e.skillid=s.skillid and EmployeeID = % s', (id,))
            skill=cursor.fetchall()
            cursor.execute('select * from EmployeeCertification e join  Certification c where e.CertificationID=c.CertificationID and  EmployeeID = % s', (id,))
            certification=cursor.fetchall()
            cursor.execute('SELECT t.TrainingName, t.TrainingDescription,et.TrainingDate FROM Training t JOIN EmployeeTraining et ON t.TrainingID = et.TrainingID JOIN Employee e ON et.EmployeeID = e.EmployeeID where  e.EmployeeID = % s', (id,))
            training=cursor.fetchall()
        return render_template('empdetails.html',emp=emp,education=education,project=project,skill=skill,certification=certification,training=training)

@app.route("/projectdetails/<int:id>")
def projectdetails(id):
    if id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Employee e JOIN EmployeeProject ep ON e.EmployeeID = ep.EmployeeID JOIN Project p ON ep.ProjectID = p.ProjectID WHERE p.ProjectID = % s', (id,))
        project = cursor.fetchall()
        if project:
            return render_template('projectdetails.html',project=project)
        else:
            return "No one in project assign"

@app.route("/skilldetails/<id>")
def skilldetails(id):
    if id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Employee e JOIN EmployeeSkill es ON e.EmployeeID = es.EmployeeID JOIN Skill s ON es.SkillID = s.SkillID WHERE s.SkillName = % s', (id,))
        skill = cursor.fetchall()
        if skill:
            return render_template('skillsdetails.html',skill=skill)
        else:
            return "No one in project assign"

@app.route("/certdetails/<id>")
def certdetails(id):
    if id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT name,CertificationName,CertificationDate FROM Employee JOIN EmployeeCertification ON Employee.EmployeeID = EmployeeCertification.EmployeeID JOIN Certification ON EmployeeCertification.CertificationID = Certification.CertificationID WHERE Certification.CertificationID= % s', (id,))
        cert = cursor.fetchall()
        if cert:
            return render_template('certdetails.html',cert=cert)
        else:
            return "No one in project assign"

@app.route("/traindetails/<id>")
def traindetails(id):
    if id:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT name,TrainingName,TrainingDescription,TrainingDate FROM Employee e JOIN EmployeeTraining et ON e.EmployeeID = et.EmployeeID JOIN Training t ON et.TrainingID = t.TrainingID WHERE t.TrainingId = % s', (id,))
        train = cursor.fetchall()
        if train:
            return render_template('traindetails.html',train=train)
        else:
            return "No one in project assign"

@app.route('/test')
def test():
    return render_template("test.html")

@app.route('/skill')
def skill():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT s.SkillName FROM Skill s LEFT JOIN EmployeeSkill es ON s.SkillID = es.SkillID AND es.EmployeeID = %s WHERE es.EmployeeID IS NULL',(session['id'],))
    skill=cursor.fetchall()
    return render_template("addskill.html",skill=skill)

@app.route('/certification')
def certification():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT c.CertificationName FROM Certification c LEFT JOIN EmployeeCertification ec ON c.CertificationID = ec.CertificationID AND ec.EmployeeID = %s WHERE ec.CertificationID IS NULL',(session['id'],))
    certification=cursor.fetchall()
    return render_template("addcertification.html",certification=certification)

@app.route('/course')
def course():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT t.TrainingID, t.TrainingName FROM Training t LEFT JOIN EmployeeTraining et ON t.TrainingID = et.TrainingID AND et.EmployeeID = %s WHERE et.EmployeeID IS NULL',(session['id'],))
    course=cursor.fetchall()
    return render_template("addcourse.html",course=course)

@app.route('/addempcourse/<int:id>',methods=['GET', 'POST'])
def empcourse(id):
    course_name = request.form['course_name']
    if course_name=='other':
        course_name=request.form['other']
    course_date = request.form['date']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Training WHERE TrainingName = %s', (course_name,))
    training = cursor.fetchone()
    if training is None:
        cursor.execute('INSERT INTO Training (TrainingName) VALUES (%s)', (course_name,))
        mysql.connection.commit()
        course_id = cursor.lastrowid
    else:
        course_id = training['TrainingID']
    cursor.execute('INSERT INTO EmployeeTraining (EmployeeID, TrainingID, TrainingDate) VALUES (%s, %s, %s)',(id, course_id, course_date))
    mysql.connection.commit()
    return redirect('/home')
        
    
@app.route('/adskill')
def adskill():
    return render_template("skill.html")   
    
@app.route('/adminskill',methods=['GET', 'POST'])
def adminskill():
    if request.method == 'POST':
        skillname = request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Skill (SkillName) VALUES (%s)', (skillname,))
        mysql.connection.commit()
        return redirect('/adminhome')
        
@app.route('/adcert')
def adcert():
    return render_template("certification.html")       

@app.route('/admincert',methods=['GET', 'POST'])
def admincert():
    if request.method == 'POST':
        certificatename = request.form['name']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Certification (CertificationName) VALUES (%s)', (certificatename,))
        mysql.connection.commit()
        return redirect('/adminhome')

@app.route('/adcourse')
def adcourse():
    return render_template("course.html")   

@app.route('/admincourse',methods=['GET', 'POST'])
def admincourse():
    if request.method == 'POST':
        coursename = request.form['name']
        description = request.form['description']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Training (TrainingName, TrainingDescription) VALUES (%s, %s)', (coursename, description))
        mysql.connection.commit()
        return redirect('/adminhome')  

@app.route('/project')
def project():
    return render_template("addproject.html")

@app.route('/addproject',methods=['GET', 'POST'])
def addproject():
    if request.method == 'POST':
        projectname = request.form['name']
        description = request.form['description']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Project (ProjectName, ProjectDescription) VALUES (%s, %s)', (projectname, description))
        mysql.connection.commit()
        return redirect('/adminhome')

@app.route('/addempcertification/<int:id>',methods=['GET', 'POST'])
def empcertification(id):
    if request.method == 'POST':
        certificate_name = request.form['certificate_name']
        if certificate_name=='other':
            certificate_name=request.form['other']
        certification_date = request.form['date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Certification WHERE CertificationName = %s', (certificate_name,))
        certificate = cursor.fetchone()
        if certificate is None:
            cursor.execute('INSERT INTO Certification (CertificationName) VALUES (%s)', (certificate_name,))
            mysql.connection.commit()
            certificate_id = cursor.lastrowid
        else:
            certificate_id = certificate['CertificationID']
        cursor.execute('INSERT INTO EmployeeCertification (EmployeeID, CertificationID, CertificationDate) VALUES (%s, %s, %s)',(id, certificate_id, certification_date))
        mysql.connection.commit()
        return redirect('/home')

@app.route('/addempskill/<int:id>',methods=['GET', 'POST'])
def empskill(id):
    if request.method == 'POST':
        inputskill = request.form['skill']
        if inputskill=='other':
            inputskill=request.form['other']
        years = request.form['years']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Skill WHERE SkillName = %s', (inputskill,))
        skill = cursor.fetchone()
        if skill is None:
            cursor.execute('INSERT INTO Skill (SkillName) VALUES (%s)', (inputskill,))
            mysql.connection.commit()
            skill_id = cursor.lastrowid
        else:
            skill_id = skill['SkillID']
        cursor.execute('INSERT INTO EmployeeSkill (EmployeeID, SkillID, YearsOfExperience) VALUES (%s, %s, %s)',(id, skill_id, years))
        mysql.connection.commit()
        return redirect('/home')
    
@app.route('/assignproject')
def assignproject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee')
    emp=cursor.fetchall()
    cursor.execute('SELECT e.name,p.ProjectID,p.ProjectName FROM Employee e JOIN EmployeeProject ep ON e.EmployeeID  = ep.EmployeeID JOIN project p ON ep.ProjectID  = p.ProjectID')
    empproject=cursor.fetchall()
    cursor.execute('SELECT * FROM Project')
    project=cursor.fetchall()
    return render_template("assignproject.html",emp=emp,project=project,empproject=empproject)

@app.route('/revokeproject')
def revokeproject():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM employee')
    emp=cursor.fetchall()
    cursor.execute('SELECT e.name,p.ProjectID,p.ProjectName FROM employee e JOIN EmployeeProject ep ON e.EmployeeID  = ep.EmployeeID JOIN project p ON ep.ProjectID  = p.ProjectID')
    empproject=cursor.fetchall()
    cursor.execute('SELECT * FROM Project')
    project=cursor.fetchall()
    return render_template("revokeproject.html",emp=emp,project=project,empproject=empproject)

@app.route('/assignproj',methods=['GET', 'POST'])
def assignproj():
    if request.method == 'POST':
        empid = request.form['employee']
        projectid = request.form['project']
        startdate = request.form['date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("INSERT INTO EmployeeProject (ProjectID, EmployeeID,StartDate) VALUES (%s, %s, %s)", (projectid, empid,startdate))
        mysql.connection.commit()
        return redirect('/adminhome')
    
@app.route('/revokeproj',methods=['GET', 'POST'])
def revokeproj():
    if request.method == 'POST':
        empid = request.form['employee']
        projectid = request.form['project']
        enddate = request.form['date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('UPDATE EmployeeProject SET EndDate = %s WHERE EmployeeID = %s AND ProjectID = %s', (enddate, empid, projectid))
        mysql.connection.commit()
        return redirect('/adminhome')

@app.route('/generatereport')
def generatereport():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Employee')
    emp=cursor.fetchall()
    return render_template("generatereport.html",emp=emp)

@app.route('/report',methods=['GET', 'POST'])
def report():
     if request.method == 'POST':
        empid = request.form['employee']
        reportname = request.form['name']
        description = request.form['description']
        reportdate = request.form['date']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('Insert into Report (ReportName,ReportDescription) VALUES (%s, %s)', (reportname,description))
        reportid = cursor.lastrowid
        cursor.execute('Insert into EmployeeReport (EmployeeID,ReportID,ReportDate) VALUES (%s, %s, %s)', (empid,reportid,reportdate))
        mysql.connection.commit()
        return redirect('/adminhome')

@app.route('/viewreport')
def viewreport():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT e.name,r.ReportID, r.ReportName, r.ReportDescription, er.ReportDate FROM Report r JOIN EmployeeReport er ON r.ReportID = er.ReportID JOIN Employee e ON er.EmployeeID = e.EmployeeID order by er.ReportDate')
    report=cursor.fetchall()
    return render_template("viewreport.html",report=report)

@app.route('/empreport')
def empreport():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT e.name,r.ReportID, r.ReportName, r.ReportDescription, er.ReportDate FROM Report r JOIN EmployeeReport er ON r.ReportID = er.ReportID JOIN Employee e ON er.EmployeeID = e.EmployeeID where e.EmployeeID = %s order by er.ReportDate',(session['id'],))
    report=cursor.fetchall()
    return render_template("viewempreport.html",report=report)

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('id', None)
    return redirect('/')
app.run(debug=True)
