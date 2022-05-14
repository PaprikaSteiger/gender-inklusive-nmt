import paramiko
import os

if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    pw = ""
    username = ""
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect("172.23.77.101", username=username, password=pw)
    sftp = ssh.open_sftp()
    files = [
        r"C:\Users\steig\Desktop\Neuer Ordner\train_data2.prepared.de.BPE.annotated",
        r"C:\Users\steig\Desktop\Neuer Ordner\validation2.de.BPE.annotated",
        r"C:\Users\steig\Desktop\Neuer Ordner\train2.de.BPE",
        r"C:\Users\steig\Desktop\Neuer Ordner\validation2.de.BPE",
    ]
    for file in files:
        remote = file.split("\\")[-1].replace("2", "3")
        sftp.put(file, remote)
    sftp.close()
    ssh.close()
#     os.system(f"sshpass -p Tierfett&6 scp -o StrictHostKeyChecking=no {file} melvinsamsonsteiger@172.23.77.101")
