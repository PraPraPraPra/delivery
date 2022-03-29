from datetime import datetime, date
import enum

class Experience(enum.Enum):
    #NAME = Maximum Years of Experience
    ZERO = 0 #No Experience
    BEGGINER = 2 # Up to two years
    INTERMEDIATE = 5 # From 2-5
    EXPERIENCED = 100 # 5+ years


resume_fernando = {
    "accenture_id": "f.d.silva@accenture.com",
    "name" : "Fernando Silva",
    'title' : 'Application Development Associate',
    'profile' : 'Fernando is an Application Development Associate from Accenture Lisbon Office where he is currently undergoing training. Fernando is also an Electrical and Computer Engineering recent graduate from Instituto Superior Técnico where he developed various projects including different technologies like C, Python, Java, JavaScript, PHP and SQL.',
    'skills' : [
        {
            'skill' : 'Python',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'C',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'Flask',
            'experience' : Experience.BEGGINER.name
        }
    ],
    'languages' : [
        {
            'language': 'English',
            'level': 'Advanced'
        },
        {
            'language': 'Portuguese',
            'level': 'Native'
        }],
    'industries' : [],
    'free_date':date(2022,12,12),
    '@timestamp': datetime.now()
}

resume_pedro = {
    "accenture_id": "pedro.henriques@accenture.com",
    "name" : "Pedro Henriques",
    'title' : 'Application Development Associate',
    'profile' : 'This is a profile.',
    'skills' : [
        {
            'skill' : 'Java',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Python',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'GCP',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'BDD/TDD',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Kubernetes/Docker',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'Jenkins',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'SonarQube',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Apigee',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'Micro Services',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Automated testing',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Selenium/Cucumber',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'Cypress',
            'experience' : Experience.BEGGINER.name
        }
    ],
    'languages' : [
        {
            'language': 'English',
            'level': 'Advanced'
        },
        {
            'language': 'Portuguese',
            'level': 'Native'
        },
        {
            'language': 'Spanish',
            'level': 'Conversational'
        }
    ],
    'industries' : [],
    'free_date':'2021-10-01',
    '@timestamp': datetime.now()
}


resume_bernia = {
    "accenture_id": "bernia.silva@accenture.com",
    "name" : "Bérnia Silva",
    'title' : 'Application Development Associate',
    'profile' : 'Experience in Java, Python, C# and general App development. Knowledge in concepts such as OOP and Google Cloud. Studied at ISEL-IPL in Computer Sciences and Multimedia. I am a very communicative person who loves to learn new things and solve problems in general.',
    'skills' : [
        {
            'skill' : 'Python',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Java',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'C#',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'PHP/SQL',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'JavaScript',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'Apigee',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Terraform',
            'experience' : Experience.BEGGINER.name
        },
        {
            'skill' : 'Jenkins',
            'experience' : Experience.EXPERIENCED.name
        },
        {
            'skill' : 'GCP',
            'experience' : Experience.BEGGINER.name
        }
    ],
    'languages' : [
        {
            'language': 'English',
            'level': ''
        },
        {
            'language': 'Portuguese',
            'level': 'Native'
        }
    ],
    'industries' : ['Altice Portugal'],
    'projects' : {
        '2008 to 2020, MEO – Altice Portugal': 'Call center team supervision. Preparing and management of improvement plans in the quality of service. Conflict resolution',
        '2017 to Current, Instituto Superior de Engenharia de Lisboa' : 'Learned about the most relevant programming paradigms such as OOP, AI, Web Development and Databases.',
        '2021-09 to 2021-10, Google Cloud Academy': 'Google Cloud Fundamentals. Architecting with Google Compute Engine. Architecting with Google Kubernetes Engine. Cloud Architecture - Design, Implement, and Manage.',
        '2021-10,  Journey to Google Cloud Initiative (Academy)' : 'Cloud – Migration Strategies. API Management and DevOps. Apigee and Terraform. Jenkins and Git. Cucumber and Selenium.'},
    'free_date':'2022-05-24',
    'updated_timestamp': datetime.now()
}

resumes = [resume_fernando, resume_pedro, resume_bernia]

mapping = {
    "properties" : {
        "skills": {
            "type": "nested",
            "properties": {
                "skill": {
                    "type": "text"
                },
                "experience": {
                    "type": "text"
                }
            }
        },
        "languages": {
            "type": "nested",
            "properties": {
                "language": {
                    "type": "text"
                },
                "level": {
                    "type": "text"
                }
            }
        }
    }
}


def get_resumes():
    return resumes

def get_mapping():
    return mapping