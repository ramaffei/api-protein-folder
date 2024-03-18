import os, time, re, requests
import asyncio
import nest_asyncio
from pyppeteer import launch
import base64

  # Apply nest_asyncio to enable nested event loops
nest_asyncio.apply()

async def fetch_blob_content(page, blob_url):
    blob_to_base64 = """
    async (blobUrl) => {
        const blob = await fetch(blobUrl).then(r => r.blob());
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onloadend = () => resolve(reader.result);
            reader.readAsDataURL(blob);
        });
    }
    """
    base64_data = await page.evaluate(blob_to_base64, blob_url)
    _, encoded = base64_data.split(',', 1)
    return base64.b64decode(encoded)

async def extract_pdb_file_download_link_and_content(url):
    browser = await launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
    page = await browser.newPage()
    await page.goto(url, {'waitUntil': 'networkidle0'})
    elements = await page.querySelectorAll('a.btn.bg-purple')
    for element in elements:
        href = await page.evaluate('(element) => element.getAttribute("href")', element)
        if 'blob:https://esmatlas.com/' in href:
            content = await fetch_blob_content(page, href)
            await browser.close()
            return href, content
    await browser.close()
    return "No PDB file link found.", None

def esmfold_api(sequence):
    url = f'https://esmatlas.com/resources/fold/result?fasta_header=%3Eunnamed&sequence=MDSSEVVKVKQASIPAPGSILSQPNTEQSPAIVLPFQFEATTFGTAETAAQVSLQTADPITKLTAPYRHAQIVECKAILTPTDLAVSNPLTVYLAWVPANSPATPTQILRVYGGQSFVLGGAISAAKTIEVPLNLDSVNRMLKDSVTYTDTPKLLAYSRAPTNPSKIPTASIQISGRIRLSKPMLIAN'
    result = asyncio.get_event_loop().run_until_complete(extract_pdb_file_download_link_and_content(url))
    if result[1]:
      pdb_str = result[1].decode('utf-8')
      return pdb_str
    else:
      return "Failed to retrieve PDB content."

sequence = "GWSTELEKHREELKEFLKKEGITNVEIRIDNGRLEVRVEGGTERLKRFLEELRQKLEKKGYTVDIKIE" #@param {type:"string"}
sequence = re.sub("[^A-Z]", "", sequence.upper())
#assert len(sequence) <= 400, "error: max length supported is 400"
pdb_filename = f"tmp/prediction_test.pdb"
if not os.path.isfile(pdb_filename):
  pdb_str = esmfold_api(sequence)
  with open(pdb_filename,"w") as out:
    out.write(pdb_str)