from datetime import date
import os


def generate_config(config,mcfg,fname, package_header=None, inicheck = False,
                    section_titles = None):
    """
    Generates a list of strings to be written and then writes them in the ini
    file

    Args:
        config - Config file dictionary created by
                 :func:`~inicheck.config.UserConfig'.
        fname - String path to the output location for the new config file.
        package_header - This is string that enables the user to customize
                         config files with their own titles. Creating a string
                         at the top that says "Configuration File for
                         <package_header>"

        inicheck - Boolean value that adds the line "file generated using
                   inicheck to config file, Default = False

    Returns:
        None
    """
    header_len = 80
    pg_sep = '#'*header_len
    #Header surround each commented titles in the ini file
    section_header = pg_sep + '\n' + ('# {0}\n') + pg_sep

    #Construct the section strings
    config_str=""
    config_str+=pg_sep

    #File header with specific package option
    config_str += "\n# Configuration File "
    if package_header != None:
        config_str+= "for {0}\n".format(package_header)

    #Add in the date generated
    config_str+= "\n# Date generated: {0}".format(date.today())

    #Generated with inicheck
    if inicheck:
        config_str+= "\n# Generated using: inicheck <filename> -w "

    config_str+="""
# For more inicheck help see:
# http://inicheck.readthedocs.io/en/latest/
"""

    #Generate the string for the file, creating them in order.
    for section in mcfg.keys():
        if section in config.keys():
            config_str+='\n'*2

            if section_titles != None:
                #Add the header
                config_str+=section_header.format(section_titles[section])
            else:
                config_str+=(pg_sep)

            config_str+='\n'
            config_str+='\n[{0}]\n'.format(section)

            #Add section items and values
            for k in sorted(config[section].keys()):
                v = config[section][k]
                if type(v) == list:
                    astr = ", ".join(str(c.strip()) for c in v)
                else:
                    astr = str(v)
                config_str+="{0:<30} {1:<10}\n".format((k+':'),astr)

    #Write out the string generated
    with open(os.path.abspath(fname),'w') as f:
        f.writelines(config_str)
        f.close()

def print_config_report(warnings, errors, logger= None):
    """
    Pass in the list of string messages generated by check_config file.
    print out in a pretty format the issues

    Args:
        warnings - List of non-critical messages returned from :func:`~utilities.check_config'.
        errors - List of critical messages returned from :func:`~utilities.check_config'.
        logger - pass in the logger function being used. If no logger is provided, print is used. Default = None

    Returns:
        None
    """

    msg = "{: <20} {: <25} {: <60}"

    #Check to see if user wants the logger or stdout
    if logger != None:
        out = logger.info
    else:
        out = print_out


    msg_len = 110
    out(" ")
    out(" ")
    out("Configuration File Status Report:")
    header = "="*msg_len
    out(header)
    any_warnings = False
    any_errors = False

    #Output warnings
    if len(warnings)>0:
        any_warnings=True
        out("WARNINGS:")
        out(" ")
        out(msg.format(" Section","Item", "Message"))
        out("-"*msg_len)
        for w in warnings:
            out(w)
        out(" ")
        out(" ")

    #Output errors
    if len(errors)>0:
        any_errors=True
        out("ERRORS:")
        out(" ")
        out(msg.format("Section","Item", "Message"))
        out("-"*msg_len)
        for e in errors:
            out(e)
        out(" ")
        out(" ")

    if not any_errors and not any_warnings:
        out("No errors or warnings were reported with the config file.\n")

def print_out(out_str):
    """
    wrapper for print so we can use either a logger or a stdout
    """
    print out_str


def print_recipe_summary(lst_recipes):
    """
    Prints out the recipes found and how they are interpretted
    """
    #len of recipe separators
    msg_len = 110
    header = "="*msg_len
    recipe_hdr = "-"*msg_len
    r_msg = "\n{: <20}\n"+recipe_hdr
    cfg_msg = "\t\t{: <20} {: <20} {: <20}"

    msg = "\t\t{: <20} {: <25}"

    print('\n\n')
    print("Recipes Summary:")
    print(header)
    for r in lst_recipes:
        print(r_msg.format(r.name))
        print("\tConditionals:")
        for n,t in r.triggers.items():
            for i,c in enumerate(t.conditions):
                if i == 0:
                    print(msg.format(n,c))
                else:
                    print(msg.format("",c))

        print_cfg_for_recipe(r.add_config,cfg_msg,hdr="\n\tAdds:")
        print_cfg_for_recipe(r.remove_config,cfg_msg,hdr="\n\tRemoves:")

    print('\n')

def print_cfg_for_recipe(cfg,fmt,hdr = None):
    if hdr !=None:
        print(hdr)

    for section in cfg.keys():
        for item, value in cfg[section].items():
            print(fmt.format(section,item,value))
