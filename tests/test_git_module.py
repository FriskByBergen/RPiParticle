import tempfile 
from unittest import TestCase
import os.path
import stat

from git.repo.base import Repo
from git import GitCommandError, NoSuchPathError, InvalidGitRepositoryError

from git_module import GitModule

def add_file( repo , name, content):
    fname = os.path.join( repo.working_tree_dir , name )
    dname = os.path.dirname( fname )
    if not os.path.isdir( dname ):
        os.makedirs( dname )

    with open(fname , "w") as f:
        f.write( content )
        
    repo.git.add( name )
    return fname
        
    

def add_executable( repo , name , content):
    fname = add_file( repo , name , content )
    
    st = os.stat( fname )
    os.chmod(fname , st.st_mode | stat.S_IEXEC)
    repo.git.add( name )



def make_origin():
    origin_root = tempfile.mkdtemp()
    origin_base = "origin"
    origin_url = os.path.join( origin_root , origin_base)
    os.makedirs( origin_url )
    repo = Repo.init( path = origin_url )

    add_file( repo , "file.txt" , "Content")
    add_file( repo , "tests/run_not_executable" , "content")
    add_file( repo , "tests/subdir/file" , "Content")
    add_executable( repo , "tests/run_OK" , "#!/bin/bash\nexit 0\n")
    add_executable( repo , "tests/run_fail" , "#!/bin/bash\nexit 1\n")

    repo.git.commit(m = "message", author="\"test <test@email.com>\"")

    repo.git.branch("version2")
    repo.git.checkout("version2")
    with open( os.path.join(origin_url , "file2.txt") , "w") as f:
        f.write("File with content")
    repo.git.add("file2.txt")
    repo.git.commit(m = "message", author="\"test <test@email.com>\"")

    return repo

    
def make_client( origin ):
    name = os.path.basename( origin.working_tree_dir )
    client_path = os.path.join( tempfile.mkdtemp() , name )
    origin_url = "file://%s" % origin.working_tree_dir
    return Repo.clone_from( origin_url , client_path )


def make_repo():
    return make_client( make_origin( ) )

def make_module():
    repo = make_repo()
    return GitModule( local_path = repo.working_tree_dir )


class GitModuleTest(TestCase):

    def startUp(self):
        pass
    
    def testCreate(self):
        with self.assertRaises(GitCommandError):
            gitm = GitModule( url = "https://does/not/exist")

        # Must have either url or local_path as arguments.
        with self.assertRaises(ValueError):
            gitm = GitModule( )

        # Must have exeactly *one* of url or local_path
        with self.assertRaises(ValueError):
            gitm = GitModule( url = "https://xxx" , local_path = "/local")

        with self.assertRaises( NoSuchPathError ):
            gitm = GitModule(local_path = "/tmp/does/not/exist")

        local_path = tempfile.mkdtemp()
        with self.assertRaises(InvalidGitRepositoryError):
            gitm = GitModule( local_path = local_path )

        

    def test_create_no_origin(self):
        origin_repo = make_origin()
        client_repo = make_client( origin_repo )

        # Clone from a repository without remote origin - should fail:
        with self.assertRaises( ValueError ):
            gitm = GitModule( local_path = origin_repo.working_tree_dir )
            



    def test_checkout(self):
        client_repo = make_repo( )

        gitm = GitModule( local_path = client_repo.working_tree_dir )
        self.assertEqual( gitm.getRoot( ) , client_repo.working_tree_dir)
        
        gitm.checkout( "master" )
        self.assertEqual( os.path.join( gitm.getRoot( ) , "file.txt" ) , gitm.absPath("file.txt") )
        self.assertEqual( gitm.getHead( )[0] , "master" )


        with self.assertRaises( IOError ):
            file2 = gitm.absPath("file2.txt")

        gitm.checkout( "version2" )
        file2 = gitm.absPath("file2.txt")
        
        with self.assertRaises(GitCommandError):
            gitm.checkout("does-not-exist")


    def test_test(self):
        gitm = make_module( )
        with self.assertRaises(IOError):
            gitm.runTests("no/such/file")
        
        with self.assertRaises(OSError):
            gitm.runTests("tests/run_not_executable")
            
        self.assertTrue( gitm.runTests("tests/run_OK"))
        self.assertFalse( gitm.runTests("tests/run_fail"))


    def test_install_files(self):
        temp = tempfile.mkdtemp()
        gitm = make_module( )
        target = os.path.join( temp , "target")
        with open( os.path.join(temp , "file") , "w") as f:
            f.write("Hello")

        with self.assertRaises(OSError):
            gitm.install( os.path.join( temp , "file"))

        gitm.install( target )
        self.assertTrue( os.path.isdir( target ))

        with self.assertRaises(IOError):
            gitm.install( target , files = ["does/not/exist"])
            
        gitm.install( target , files = ["tests/run_OK",
                                        "tests/run_fail"])
        self.assertTrue( os.path.isfile( os.path.join( target , "tests/run_OK")))
        self.assertTrue( os.path.isfile( os.path.join( target , "tests/run_fail")))


    def test_install_directories(self):
        temp = tempfile.mkdtemp()
        gitm = make_module( )
        target = os.path.join( temp , "target")

        gitm.install( target , directories = ["tests/subdir"])
        self.assertTrue( os.path.isfile( os.path.join( target , "tests/subdir/file")))
        self.assertFalse( os.path.isfile( os.path.join( target , "tests/run_OK")))

        gitm.install( target , directories = ["tests"])
        self.assertTrue( os.path.isfile( os.path.join( target , "tests/run_OK")))

        gitm.install( target , 
                      directories = ["tests"],
                      files = ["tests/run_OK", "tests/run_fail"])
    
