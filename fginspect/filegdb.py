import arcpy


class FileGDB:
    def __init__(self, fgdb_path):
        self.fgdb_path = fgdb_path
        self.rpt_file = None
        self.setenv()

    @property
    def rpt_file_path(self):
        return self.fgdb_path.replace(".gdb", ".txt")

    def info(self):
        print(self.fgdb_path)
        print(self.rpt_file_path)

    def setenv(self):
        print("\nSetting arcpy environment ...")
        arcpy.env.workspace = self.fgdb_path
        arcpy.env.overwriteOutput = True

    def process(self):
        self.open_report_file()

        title = "Geodatabase: %s\n" % self.fgdb_path
        self.write_it(self.rpt_file, title)

        self.process_feature_datasets()
        self.process_feature_classes()
        self.process_feature_classes_fields()
        self.process_tables()
        self.process_tables_fields()
        self.process_domains()
        self.process_subtypes()
        self.process_relationships()

        self.close_report_file()

    def process_feature_datasets(self):
        print("Processing datasets")

        self.write_it(self.rpt_file, "FEATURE DATASETS:")
        self.write_it(
            self.rpt_file, "==============================================================================\n")
        self.write_it(self.rpt_file, "{0:30} {1:30} {2:30} {3:70}".format(
            "Dataset Name", "Dataset Type", "Spatial Reference", "Extent"))
        self.write_it(self.rpt_file, "{0:30} {1:30} {2:30} {3:70}".format(
            "------------", "------------", "-----------------", "------"))

        fdslist = arcpy.ListDatasets()
        for fds in fdslist:
            desc = arcpy.Describe(fds)
            ds_type = desc.datasetType
            ds_crs = desc.spatialReference.name
            ds_extent = "{0:12.3f} {1:12.3f} {2:12.3f} {3:12.3f}".format(
                desc.extent.XMin, desc.extent.YMin, desc.extent.XMax, desc.extent.YMax)
            self.write_it(self.rpt_file, "{0:30} {1:30} {2:30} {3:70}".format(
                fds, ds_type, ds_crs, ds_extent))

    def process_feature_classes(self):
        print("Processing feature classes")

        self.write_it(self.rpt_file, "\nFEATURE CLASSES:")
        self.write_it(
            self.rpt_file, "==============================================================================")
        self.write_it(self.rpt_file, "\n{0:30} {1:30} {2:10} {3:6} {4:7}".format(
            "Feature Dataset", "Feature Class", "Geometry", "Fields Count", "Records Count"))
        self.write_it(self.rpt_file, "{0:30} {1:30} {2:10} {3:6} {4:7}".format(
            "---------------", "-------------", "--------", "------------", "-------------"))

        fdslist = [""] + arcpy.ListDatasets()
        for fds in fdslist:
            fclist = arcpy.ListFeatureClasses("*", "", fds)
            for fc in fclist:
                desc = arcpy.da.Describe(fc)

                try:
                    shape_type = desc['shapeType']

                    fields_count = len(arcpy.ListFields(fc))
                    records_count = str(arcpy.GetCount_management(fc))

                    self.write_it(self.rpt_file, "{0:30} {1:30} {2:10} {3:6} {4:7}".format(
                        fds, fc, shape_type, fields_count, int(records_count)))

                    fds = ""
                except:
                    print(fc)
                    print("An exception occurred")

    def process_feature_classes_fields(self):
        print("Processing feature classes fields")

        self.write_it(self.rpt_file, "\nFEATURE CLASSES - FIELDS:")
        self.write_it(
            self.rpt_file, "==============================================================================")
        self.write_it(self.rpt_file, "\n%-25s %-25s %-30s %-30s %-15s %s" % ("Feature Dataset",
                                                                             "Feature Class", "Field Name", "Field Alias", "Field Type", "Field Domain"))
        self.write_it(self.rpt_file,   "%-25s %-25s %-30s %-30s %-15s %s" % ("---------------",
                                                                             "-------------", "----------", "-----------", "----------", "------------"))

        fdslist = [""] + arcpy.ListDatasets()
        for fds in fdslist:
            fclist = arcpy.ListFeatureClasses("*", "", fds)

            for fc in fclist:
                try:
                    fields = arcpy.ListFields(fc)

                    for field in fields:
                        self.write_it(self.rpt_file, "%-25s %-25s %-30s %-30s %-15s %s" %
                                      (fds, fc, field.name, field.aliasName, field.type, field.domain))
                        fc = ""
                        fds = ""
                except:
                    print(fc)
                    print("An exception occurred")

    def process_tables(self):
        print("Processing tables")

        self.write_it(self.rpt_file, "\nTables:")
        self.write_it(self.rpt_file, "=======")
        self.write_it(self.rpt_file, "\n%-30s %-10s %-10s" %
                      ("Table Name", "Fields Count", "Records Count"))
        self.write_it(self.rpt_file, "%-30s %-10s %-10s" %
                      ("----------", "------------", "-------------"))

        tablelist = arcpy.ListTables()
        for table in tablelist:
            fields_count = len(arcpy.ListFields(table))
            records_count = str(arcpy.GetCount_management(table))
            self.write_it(self.rpt_file, "{0:30} {1:10} {2:10}".format(
                table, fields_count, int(records_count)))

    def process_tables_fields(self):
        print("Processing tables fields")

        self.write_it(self.rpt_file, "\nTABLES - FIELDS:")
        self.write_it(
            self.rpt_file, "==============================================================================")
        self.write_it(self.rpt_file, "\n%-30s %-30s %-30s %-15s %s" %
                      ("Table Name", "Field Name", "Field Alias", "Field Type", "Field Domain"))
        self.write_it(self.rpt_file, "%-30s %-30s %-30s %-15s %s" %
                      ("----------", "----------", "-----------", "----------", "------------"))

        tablelist = arcpy.ListTables()
        for table in tablelist:
            desc = arcpy.Describe(table)

            for field in desc.fields:
                self.write_it(self.rpt_file, "%-30s %-30s %-30s %-15s %s" %
                              (table, field.name, field.aliasName, field.type, field.domain))
                table = ''

    def process_domains(self):
        print("Processing domains")

        self.write_it(self.rpt_file, "\nDOMAINS:")
        self.write_it(
            self.rpt_file, "==============================================================================")
        self.write_it(self.rpt_file, "\n%-30s %-10s %-40s" %
                      ("Domain Name", "Code", "Description"))
        self.write_it(self.rpt_file, "%-30s %-10s %-40s" %
                      ("-----------", "----", "-----------"))

        domains = arcpy.da.ListDomains(self.fgdb_path)
        for domain in domains:
            domain_name = domain.name
            domain_type = domain.domainType
            if domain.domainType == 'CodedValue':
                coded_values = domain.codedValues
                for code, desc in coded_values.items():
                    self.write_it(self.rpt_file, '%-30s %-10s %-40s' %
                                  (domain_name, code, desc))
                    domain_name = ""
            elif domain.domainType == 'Range':
                self.write_it(self.rpt_file, '%-30s %-10s %-40s' %
                              (domain.name, domain.range[0], domain.range[1]))
                domain_name = ""

    def process_subtypes(self):
        print("Processing subtypes")

        self.write_it(self.rpt_file, "\nSUBTYPES:")
        self.write_it(
            self.rpt_file, "==============================================================================")
        self.write_it(self.rpt_file, "\n%-20s %-20s %-20s %-5s %-20s" %
                      ("Feature Dataset", "Feature Class", "Field", "Code", "Description"))
        self.write_it(self.rpt_file, "%-20s %-20s %-20s %-5s %-20s" %
                      ("--------------------", "--------------------", "--------------------", "-----", "--------------------"))

        fdslist = [""] + arcpy.ListDatasets()
        for fds in fdslist:

            fclist = arcpy.ListFeatureClasses("*", "", fds)

            for fc in fclist:
                try:
                    subtypes_dict = arcpy.da.ListSubtypes(fc)

                    idx = 0
                    for stcode, stdict in list(subtypes_dict.items()):
                        subtype_field = stdict['SubtypeField']
                        subtype_name = stdict['Name']

                        if subtype_field != "":
                            if idx == 0:
                                self.write_it(
                                    self.rpt_file, "%-20s %-20s %-20s %-5s %-20s" % (fds, fc, subtype_field, stcode, subtype_name))
                            else:
                                self.write_it(
                                    self.rpt_file, "%-20s %-20s %-20s %-5s %-20s" % ('', '', '', stcode, subtype_name))
                        idx = idx + 1
                except:
                    print(fc)
                    print("An exception occurred")

    def process_relationships(self):
        print("Processing relationships ...")

        self.write_it(self.rpt_file, "\nRELATIONSHIPS:")
        self.write_it(
            self.rpt_file, "==============================================================================")
        self.write_it(self.rpt_file, "\n%-50s %-30s %-30s %-30s %-30s %-20s" %
                      ("Relationship Name", "Origin Table", "Origin Key", "Foreign Table", "Foreign Key", "Cardinality"))
        self.write_it(self.rpt_file, "%-50s %-30s %-30s %-30s %-30s %-20s" %
                      ("-----------------", "------------", "----------", "-------------", "-----------", "-----------"))

        relClassSet = self.get_relationship_classes()
        for relClass in relClassSet:
            rel = arcpy.Describe(relClass)

            rel_origin_table = rel.originClassNames[0]
            rel_destination_table = rel.destinationClassNames[0]

            rel_primary_key = rel.originClassKeys[0][0]
            rel_foreign_key = rel.originClassKeys[1][0]

            # convert primary/foreign key to uppercase if not found
            if rel_primary_key not in [field.name for field in arcpy.ListFields(rel_origin_table)]:
                rel_primary_key = rel.originClassKeys[0][0].upper()

            if rel_foreign_key not in [field.name for field in arcpy.ListFields(rel_destination_table)]:
                rel_foreign_key = rel.originClassKeys[1][0].upper()

            self.write_it(self.rpt_file, "%-50s %-30s %-30s %-30s %-30s %-20s" % (rel.name,
                                                                                  rel_origin_table, rel_primary_key, rel_destination_table, rel_foreign_key, rel.cardinality))

    def get_relationship_classes(self):

        # get featureclasses outside of datasets
        fc_list = arcpy.ListFeatureClasses("*")

        # get fetatureclasses within datasets
        fds_list = arcpy.ListDatasets("*", "Feature")
        for fds in fds_list:
            fc_list += arcpy.ListFeatureClasses("*", "", fds)

        # get tables
        fc_list += arcpy.ListTables("*")

        # create relationship classes set
        relClasses = set()
        for i, fc in enumerate(fc_list):
            desc = arcpy.Describe(fc)
            try:
                for j, rel in enumerate(desc.relationshipClassNames):
                    relClasses.add(rel)
            except:
                print(fc)
                print("An exception occurred")

        return relClasses

    def write_it(self, out_file, out_text):
        out_text = out_text + '\n'
        enc_text = out_text.encode("utf8")
        out_file.write(enc_text)

    def open_report_file(self):
        self.rpt_file = open(self.rpt_file_path, "wb")

    def close_report_file(self):
        self.rpt_file.close()
