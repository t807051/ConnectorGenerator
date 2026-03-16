import os

# BASEDIR = r"C:\github\Insight10.8\Insight"
BASEDIR = r"C:\TEMP"
CONNECTORDIR = os.path.join(BASEDIR, "connectors")
BUILDDIR = os.path.join(BASEDIR, "build")
KBDIR = os.path.join(BASEDIR, r"knowledgebases\com.telus.falcon.knowledgebase")
MODELDIR = os.path.join(KBDIR, "model")
CALLDIR = os.path.join(MODELDIR, r"da\call")
QADIR = os.path.join(MODELDIR, r"qa\da")

# TEMPLATEDIR = r"C:\cb\Insight10.8\Template"
TEMPLATEDIR = r"C:\github\t807051\ConnectorGenerator\Template"
TEMPLATECONNECTORDIR = os.path.join(TEMPLATEDIR, "connectors")
TEMPLATEBUILDDIR = os.path.join(TEMPLATEDIR, "build")
TEMPLATEKBCALLDIR = os.path.join(
    TEMPLATEDIR,
    r"knowledgebases\com.telus.falcon.knowledgebase\models\da\call",
)
TEMPLDATEKBQADIR = os.path.join(
    TEMPLATEDIR,
    r"knowledgebases\com.telus.falcon.knowledgebase\models\qa\da",
)

TEMPLATE_NAME = "svcqualification"

TEMPLATE_CONNECTOR_JAVA = os.path.join(
    TEMPLATECONNECTORDIR,
    "com.telus.connector." + TEMPLATE_NAME,
    "src",
    "com",
    "telus",
    "connector",
    TEMPLATE_NAME,
    "call",
    "TemplateConnector.java.txt",
)
TEMPLATE_FACTORY_JAVA = os.path.join(
    TEMPLATECONNECTORDIR,
    "com.telus.connector." + TEMPLATE_NAME,
    "src",
    "com",
    "telus",
    "connector",
    TEMPLATE_NAME,
    "factories",
    "TemplateFactory.java.txt",
)
TEMPLATE_EXCEPTION_JAVA = os.path.join(
    TEMPLATECONNECTORDIR,
    "com.telus.connector." + TEMPLATE_NAME,
    "src",
    "com",
    "telus",
    "connector",
    TEMPLATE_NAME,
    "exception",
    "TemplateException.java.txt",
)
TEMPLATE_CONVERTER_JAVA = os.path.join(
    TEMPLATECONNECTORDIR,
    "com.telus.connector." + TEMPLATE_NAME,
    "src",
    "com",
    "telus",
    "connector",
    TEMPLATE_NAME,
    "converter",
    "TemplateConverter.java.txt",
)
TEMPLATE_ICONFIG_JAVA = os.path.join(
    TEMPLATECONNECTORDIR,
    "com.telus.connector." + TEMPLATE_NAME + ".config",
    "src",
    "com",
    "telus",
    "connector",
    TEMPLATE_NAME,
    "ITemplateConfigurationComponent.java.txt",
)
TEMPLATE_CONFIG_JAVA = os.path.join(
    TEMPLATECONNECTORDIR,
    "com.telus.connector." + TEMPLATE_NAME + ".config",
    "src",
    "com",
    "telus",
    "connector",
    TEMPLATE_NAME,
    "TemplateConfigurationComponent.java.txt",
)
TEMPLATE_SPEC_MD = os.path.join(TEMPLATEDIR, "ConnectorSpecTemplate.md.txt")

