from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

jobs = [
    {'title': 'Database listing', 'url': 'https://www.freelancer.com/projects/dot-net/database-listing/',
     'days_left': '5 days left',
     'description': 'Requirement is to list all the contents in excel files which is in CSV format to user friendly GUI window using Visual basic or , .net.',
     'skills': ['.NET', 'Visual Basic']},
    {'title': 'Classic ASP and ASP.Net Developer #3',
     'url': 'https://www.freelancer.com/projects/dot-net/classic-asp-asp-net-developer/', 'days_left': '5 days left',
     'description': 'looking for long term developer that have skills and experience in Classic ASP and ASP.Net we have lots of web site that need maintenance, and some new web site to build from zero/ send us Classic ASP websites that you worked on as portfolio. also we have php and wp site if you have any more skills',
     'skills': ['.NET', 'ASP', 'ASP.NET', 'Visual Basic']},
    {'title': 'Build a Software to Tag PDF Files',
     'url': 'https://www.freelancer.com/projects/javascript/build-software-tag-pdf-files/', 'days_left': '5 days left',
     'description': 'We process PDF files and deliver the files to the existing clients. we are scaling up our ventures to make this more efficient and easy. Tagging an existing PDF according to our norms would make it more quicker. Further details can be briefed later. This requires basic knowledge about PDF files and how Tagging in PDF works.',
     'skills': ['.NET', 'Java', 'Javascript', 'PDF', 'Software Development']},
    {'title': 'Simple Online Accounting Software',
     'url': 'https://www.freelancer.com/projects/php/simple-online-accounting-software/', 'days_left': '5 days left',
     'description': 'We need a simple Online Accounting Software to use for our Medical Lab. We have 3 branches and each of the branch can use this software using their own login. There are two roles. Lab Role and Admin Role. Attached is the mock wireframe of the app to be developed. Preferably .Net Application. MySql. Better to have responsive design. Only used by internal employees.',
     'skills': ['.NET', 'Angular.js', 'Full Stack Development', 'MySQL', 'PHP']},
    {'title': '.net winforms wysiwyg editor for html',
     'url': 'https://www.freelancer.com/projects/html/net-winforms-wysiwyg-editor-for/', 'days_left': '5 days left',
     'description': 'Need fully working form which includes wysiwyg html editor. Must be able to work with modern html (5) and be maintainable. So happy if its java based, but all forms must open without windows warnings etc. Only contact me if you did this already and can show me today.',
     'skills': ['.NET', 'ASP.NET', 'C# Programming', 'HTML', 'Javascript']},
    {'title': 'Require Desktop Application Developer for Development of Desktop base Scrapping Application',
     'url': 'https://www.freelancer.com/projects/php/require-desktop-application-developer/',
     'days_left': '5 days left',
     'description': 'Require Desktop Application Developer for Development of Desktop base Scrapping Application.',
     'skills': ['.NET', 'ASP.NET', 'C# Programming', 'PHP', 'Software Architecture']},
    {'title': 'I need help in designing a Desktop based WPF application in MVVM architecture.',
     'url': 'https://www.freelancer.com/projects/software-architecture/need-help-designing-desktop-based/',
     'days_left': '5 days left',
     'description': "I have create the base and have almost created all the view and view models..But currently I am confused how to proceed .This application has multiple Tab controls each bound to a VM and it's Content is set as Corresponding [login to view URL] I am facing few [login to view URL] bid if you are confident about this..I have not used PRISM in this..and would want to avoid it..Need a simple appro...",
     'skills': ['.NET', 'C# Programming', 'Software Architecture', 'Windows API', 'Windows Desktop']},
    {'title': 'Looking Expert who can able to develop scrapping tools',
     'url': 'https://www.freelancer.com/projects/php/looking-expert-who-can-able/', 'days_left': '4 days left',
     'description': 'we are Looking Expert who can able to develop scrapping tools desktop base [login to view URL] more details share your work experiance',
     'skills': ['.NET', 'C# Programming', 'PHP', 'Software Architecture', 'Web Scraping']},
    {'title': 'Hire .Net MVC Developer',
     'url': 'https://www.freelancer.com/projects/c-sharp-programming/hire-net-mvc-developer/',
     'days_left': '4 days left',
     'description': 'Hi, we would like to hire a .net mvc developer to continue extend on an existing web application designed in .Net, MVC, Entity framework, Bootstrap, MSSQL and SSRS. The application is used to insert and create products related to construction (products include aluminium, pvc, wood apertures etc..). It is used for business analytics and also quote generation. Experience in TelerikUI is a plus.',
     'skills': ['.NET', 'ASP.NET', 'C# Programming', 'Microsoft SQL Server', 'MVC']},
    {'title': 'Blockchain Development', 'url': 'https://www.freelancer.com/projects/css/blockchain-development/',
     'days_left': '4 days left',
     'description': "Looking to bring on additional developers proficient in C#, .NET Core, and React JS to assist with the development of RadiumCore and the Radium SmartChain. For more information regarding our project, please see below. Website: [login to view URL] Development and Expansion Roadmap: [login to view URL] The aforementioned road-map should give you an idea of the projects you'll be working on. P...",
     'skills': ['.NET', 'Blockchain', 'C# Programming', 'CSS', 'React.js']}
]

if __name__ == "__main__":

    db_host = 'localhost'
    db_name = "jobs"
    coll_name = "jobs"

    client = MongoClient(db_host)
    db = client[db_name]

    coll = db.get_collection(coll_name)

    # insert or update
    # jobs = []

    for job in jobs:
        job_doc = job.copy()
        job_doc["_id"] = job_doc["url"]
        #jobs.append(job)
        try:
            coll.insert(job_doc)
        except DuplicateKeyError as dup_err:
            print("pk {} already exists".format(job_doc["_id"]))

    # coll.insert(jobs)

