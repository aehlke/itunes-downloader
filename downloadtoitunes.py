import os
import sys
import urllib2
import shutil
from glob import glob
#from optparse import OptionParser
from urlparse import urlsplit
import subprocess
#import Tkinter
import fnmatch
import tempfile


#cwd = os.getcwd()


def chunk_report(bytes_so_far, chunk_size, total_size):
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    sys.stdout.write("Downloaded %d of %d bytes (%0.2f%%)\r" % 
        (bytes_so_far, total_size, percent))

    if bytes_so_far >= total_size:
       sys.stdout.write('\n')

def chunk_read(response, output_file_path, chunk_size=4096, report_hook=None):
    total_size = response.info().getheader('Content-Length').strip()
    total_size = int(total_size)
    bytes_so_far = 0

    output_file = open(output_file_path, 'wb')

    try:
        while 1:
            chunk = response.read(chunk_size)
            output_file
            bytes_so_far += len(chunk)
        
            if not chunk:
                break
            
            output_file.write(chunk)

            if report_hook:
                report_hook(bytes_so_far, chunk_size, total_size)
    finally:
        output_file.close()

    return bytes_so_far


def url_to_name(url):
    return os.path.basename(urlsplit(url)[2])

def download(url, download_dir, local_file_name=None):
    '''Returns the name of the downloaded file.'''
    local_name = url_to_name(url)
    req = urllib2.Request(url)
    try:
        r = urllib2.urlopen(req)
    except ValueError:
        print 'Invalid URL.'
        exit(1)
    if r.info().has_key('Content-Disposition'):
        # If the response has Content-Disposition, we take file name from it
        local_name = r.info()['Content-Disposition'].split('filename=')[1]
        if local_name[0] == '"' or local_name[0] == "'":
            local_name = local_name[1:-1]
    elif r.url != url: 
        # if we were redirected, the real file name we take from the final URL
        local_name = url_to_name(r.url)
    if local_file_name: 
        # we can force to save the file as specified name
        local_name = local_file_name
    chunk_read(r, os.path.join(download_dir, local_name),\
            report_hook=chunk_report, chunk_size=1024)
    return local_name


def add_directory_to_itunes(cwd, dir_path):
    #dir_alias = Alias(dir_path)
    #itunes.add(dir_alias, to=itunes.playlists['Library'])
    #files = [Alias(u'/Users/foo/some.mp3'), Alias(u'/Users/foo/another.mp3'), ...]
    #itunes.add(files, to=itunes.playlists['Library'])
    try:
        #script_path = os.path.join(os.path.dirname(__file__), 'addToITunesLibrary')
        script_path = os.path.join(cwd, 'addToITunesLibrary')
        ret_code = subprocess.call('"' + script_path + '" "' + dir_path + '"', shell=True)
        if ret_code < 0:
            print >>sys.stderr, 'Child was terminated by signal', -ret_code
            #exit(1)
    except OSError, e:
        print >>sys.stderr, 'Execution failed:', e
        #exit(1)

def get_clipboard():
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    ret_code = p.wait()
    data = p.stdout.read()
    return data



#def get_preferences():
#    'Gets the contents of the prefs file, if it exists.'
#    if os.path.exists(cwd + 'prefs'):
#        f = open(cwd + 'prefs', 'r')
#        contents = f.read()
#        f.close()
#        return contents
#    else:
#        return ''


#def set_preferences(contents):
#    f = open(cwd + 'prefs', 'w')
#    f.write(contents)
#    f.close()


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: %s archive-URL' % sys.argv[0])
    url = sys.argv[1]

    cwd = os.path.join(os.path.dirname(__file__))

#    clipboard = get_clipboard()
#    if clipboard:
#        url = clipboard
#    else:
#        print 'No URL copied in clipboard.'
#        exit(0)
    
    # initialize the download directory
    print 'Initializing...'
    download_dir_path = tempfile.mkdtemp(prefix='tmp3')

    # download the archive
    print 'Downloading archive...'
    archive_name = download(url, download_dir_path)
    archive_path = os.path.join(download_dir_path, archive_name)

    # extract it, using the 'e' ruby script, to the download directory
    print 'Extracting archive...'
    try:
        ret_code = subprocess.call('"'+os.path.join(cwd, 'e')+'"' +\
                ' ' + archive_name, cwd=download_dir_path, shell=True)
        if ret_code < 0:
            print >>sys.stderr, 'Child was terminated by signal', -ret_code
            shutil.rmtree(download_dir_path)
            exit(1)
    except OSError, e:
        print >>sys.stderr, 'Execution failed:', e
        shutil.rmtree(download_dir_path)
        exit(1)

    # delete the archive
    print 'Deleting archive...'
    os.remove(archive_path)

    # delete any m3u playlist files, to avoid duplication
    #FIXME
    #for playlist_file in glob(download_dir_path + '*.m3u'):
    #    os.remove(playlist_file)
    #    i += 1
    print 'Deleting any playlist files...'
    i = 0
    for root, dirnames, filenames in os.walk(download_dir_path):
        for filename in fnmatch.filter(filenames, '*.m3u'):
            os.remove(os.path.join(root, filename))
            i += 1
    print '({0} deleted)'.format(i)

    # add all files in the 'downloading' dir to iTunes
    print 'Adding to iTunes Library...'
    add_directory_to_itunes(cwd, download_dir_path)
    
    # delete the downloaded files
    print 'Cleaning up...'
    shutil.rmtree(download_dir_path)

    print 'Done!'

    exit(0)



if __name__ == "__main__":
    #cwd = sys.argv[1]
    #if cwd[:4] == '.app':
    #    cwd = cwd + '/Contents/Resources' #os.path.join(cwd, '/Contents/Resources')
    main()


