import gdown

url = 'https://drive.google.com/file/d/1n8sEgL1jDYxhDg5hLCs52okNmc3y7Kpq/view?usp=sharing'
output = 'data/data.csv'
gdown.download(url, output, quiet=False)
