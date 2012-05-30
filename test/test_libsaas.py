import pkgutil
import unittest


def get_suite():
    modules = []
    moditer = pkgutil.iter_modules(['test'])

    for importer, modname, is_package in moditer:
        module = importer.find_module(modname).load_module(modname)
        modules.append(module)

    suites = [unittest.TestLoader().loadTestsFromModule(module)
              for module in modules]
    return unittest.TestSuite(suites)


def main():
    unittest.TextTestRunner(verbosity=2).run(get_suite())


if __name__ == "__main__":
    main()
