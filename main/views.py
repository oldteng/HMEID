from django.shortcuts import render
import json
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, FileResponse
from main.models import *

# Create your views here.

def index(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')

def help(request):
    return render(request,'help.html')

def stats(request):
    return render(request,'statistics.html')

def download(request):
    return render(request,'download.html')

def big_file_download(request, file_name):
    the_file_name = "/home/website/HMEID/media/" + file_name
    response = FileResponse(open(the_file_name, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
    return response

def search(request):
    return render(request,'result.html',{'search_request':request.META["QUERY_STRING"]})

def construct_query_dict(query):
    json_out = {}
    json_out["data"] = [dict(zip(["id","chrom","position","type","length","subfamily","AC","AN","AF"],[record.site_name,record.chrom,record.position,record.site_type,record.site_length,record.subfamily,record.Total_AC,record.Total_AN,record.Total_AF])) for record in query]
    return json_out

def search_json(request):
    values = request.GET
    chrom = values.get('ChromInput',default="Null")
    start = values.get('StartInput',default="Null")
    end = values.get('EndInput',default="Null")
    gene = values.get('GeneInput',default="Null")
    mei_type = values.get('MEIType1',default="All")
    LenLow = values.get('LenLow',default="Null")
    LenHigh = values.get('LenHigh',default="Null")
    ACLow = values.get('ACLow',default="Null")
    ACHigh = values.get('ACHigh',default="Null")
    ANLow = values.get('ANLow',default="Null")
    ANHigh = values.get('ANHigh',default="Null")
    AFLow = values.get('AFLow',default="Null")
    AFHigh = values.get('AFHigh',default="Null")
    ASSESSLow = values.get('assess',default="Null")
    SRLow = values.get('sr',default="Null")
    LPLow = values.get('lp',default="Null")
    RPLow = values.get('rp',default="Null")
    query = Q()
    if gene !="Null" and gene !="":
        query = query & (Q(gene__iexact=gene)|Q(ensembl__iexact=gene))
    elif chrom != "Null" and chrom !="":
        query = query & Q(chrom__exact=chrom)
        if start != "Null" and start != "":
            if end == "Null" or end == "":
                query = query & Q(position__exact=int(start))
            else:
                query = query & Q(position__gte=int(start),position__lte=int(end))
    if mei_type != 'All':
        query = query & Q(site_type__exact=mei_type)
    if LenLow != "Null" and LenLow != "":
        query = query & Q(site_length__gt=float(LenLow))
    if LenHigh != "Null" and LenHigh != "":
        query = query & Q(site_length__lte=float(LenHigh))
    if ACLow != "Null" and ACLow != "":
        query = query & Q(Total_AC__gt=float(ACLow))
    if ACHigh != "Null" and ACHigh != "":
        query = query & Q(Total_AC__lte=float(ACHigh))
    if ANLow != "Null" and ANLow != "":
        query = query & Q(Total_AN__gt=float(ANLow))
    if ANHigh != "Null" and ANHigh != "":
        query = query & Q(Total_AN__lte=float(ANHigh))
    if AFLow != "Null" and AFLow != "":
        query = query & Q(Total_AF__gt=float(AFLow))
    if AFHigh != "Null" and AFHigh != "":
        query = query & Q(Total_AF__lte=float(AFHigh))
    if ASSESSLow != "Null" and ASSESSLow != "":
        query = query & Q(assess__gte=float(ASSESSLow))
    if SRLow != "Null" and SRLow != "":
        query = query & Q(sr__gte=float(SRLow))
    if LPLow != "Null" and LPLow != "":
        query = query & Q(lp__gte=float(LPLow))
    if RPLow != "Null" and RPLow != "":
        query = query & Q(rp__gte=float(RPLow))
    data = Sites.objects.filter(query).order_by('chrom','position')
    query_dict = construct_query_dict(data)
    return JsonResponse(query_dict)

def site_json(request,site_name):
    entry = Sites.objects.get(pk=site_name)
    snps = LD_SNP.objects.filter(site_name__exact=site_name)
    return_text = ''
    return_text += '<h4 style="font-weight:bold">Site profile</h4><br>'
    return_text += ('<p>Position: '+entry.chrom+':'+str(entry.position)+'</p>')
    return_text += ('<p>Type: '+entry.site_type+'</p>')
    return_text += ('<p>Subfamily: '+entry.subfamily+'</p>')
    if entry.strand == '+':
        return_text += ('<p>Strand: <span class="glyphicon glyphicon-plus" aria-hidden="true"></span></p>')
    else:
        return_text += ('<p>Strand: <span class="glyphicon glyphicon-minus" aria-hidden="true"></span></p>')
    if not entry.site_length is None:
        return_text += ('<p>Length: '+str(entry.site_length)+'</p>')
    else:
        return_text += ('<p>Length: Unknown</p>')
    if entry.gene:
        return_text += ('<p>Aligned Gene: '+entry.gene+'/'+entry.ensembl+'</p>')
    else:
        return_text += ('<p>Aligned Gene: -</p>')
    return_text += ('<p>Consequence: '+entry.consequence+'</p>')
    return_text += ('<p>Endonuclease site: '+entry.insert_site+'</p>')
    if not entry.istp is None:
        if entry.istp == -1:
            return_text += ('<p>5\' inversion: Not inverted</p>')
        elif entry.istp == 0:
            return_text += ('<p>5\' inversion: Not twin-primed site</p>')
        else:
            return_text += ('<p>5\' inversion: '+str(entry.istp)+'</p>')
    if snps.exists():
        return_text += ('<p>GWAS SNP LD: ')
        for snp in snps:
            return_text += ('&nbsp; <button type="button" class="btn btn-primary btn-sm" onclick="window.location.href=\'https://www.ebi.ac.uk/gwas/variants/'+snp.snp_id+'\'" data-tippy-content="'+snp.disease+' | p-value='+str(snp.pvalue)+'">'+snp.snp_id+'</button>')
        return_text += ('</p>')

    return_text += '<hr><h4 style="font-weight:bold">Site quality</h4><br>'
    return_text += '<table class="table table-striped table-hover"><thead><tr><th>ASSESS</th><th>SR</th><th>LP</th><th>RP</th></tr></thead><tbody>'
    return_text += ('<tr><td>'+'</td><td>'.join([str(entry.assess),str(entry.sr),str(entry.lp),str(entry.rp)])+'</td></tr>')
    return_text += '</tbody></table>'

    return_text += '<hr><div id="pop_plots"><h4 style="font-weight:bold">Population plot</h4><br><div id="super_plot" style="width: 500px; height: 300px"></div><div id="sub_plot" style="width: 500px; height: 300px"></div><div id="nyuwa_plot" style="width: 500px; height: 300px"></div>'

    return_text += '<hr></div><h4 style="font-weight:bold">Population table</h4><br>'
    return_text += '<table class="table table-striped table-hover"><thead><tr><th>Population</th><th>AC</th><th>AN</th><th>AF</th></tr></thead><tbody>'
    return_text += ('<tr><th>Total</th><td>'+'</td><td>'.join([str(entry.Total_AC),str(entry.Total_AN),str(entry.Total_AF)])+'</td></tr>')
    return_text += ('<tr><th>1KGP</th><td>'+'</td><td>'.join([str(entry.KGP_AC),str(entry.KGP_AN),str(entry.KGP_AF)])+'</td></tr>')
    return_text += ('<tr><th>NyuWa</th><td>'+'</td><td>'.join([str(entry.CN3270_AC),str(entry.CN3270_AN),str(entry.CN3270_AF)])+'</td></tr>')
    return_text += ('<tr><th>AFR</th><td>'+'</td><td>'.join([str(entry.AFR_AC),str(entry.AFR_AN)])+'</td><td id="AFR_AF">'+str(entry.AFR_AF)+'</td></tr>')
    return_text += ('<tr><th>AMR</th><td>'+'</td><td>'.join([str(entry.AMR_AC),str(entry.AMR_AN)])+'</td><td id="AMR_AF">'+str(entry.AMR_AF)+'</td></tr>')
    return_text += ('<tr><th>EAS</th><td>'+'</td><td>'.join([str(entry.EAS_AC),str(entry.EAS_AN)])+'</td><td id="EAS_AF">'+str(entry.EAS_AF)+'</td></tr>')
    return_text += ('<tr><th>EAS (1KGP)</th><td>'+'</td><td>'.join([str(entry.EAS_1KGP_AC),str(entry.EAS_1KGP_AN)])+'</td><td id="EAS_1KGP_AF">'+str(entry.EAS_1KGP_AF)+'</td></tr>')
    return_text += ('<tr><th>EUR</th><td>'+'</td><td>'.join([str(entry.EUR_AC),str(entry.EUR_AN)])+'</td><td id="EUR_AF">'+str(entry.EUR_AF)+'</td></tr>')
    return_text += ('<tr><th>SAS</th><td>'+'</td><td>'.join([str(entry.SAS_AC),str(entry.SAS_AN)])+'</td><td id="SAS_AF">'+str(entry.SAS_AF)+'</td></tr>')
    return_text += ('<tr><th>CHB and CHS (1KGP)</th><td>'+'</td><td>'.join([str(entry.CHB_and_CHS_1KGP_AC),str(entry.CHB_and_CHS_1KGP_AN),str(entry.CHB_and_CHS_1KGP_AF)])+'</td></tr>')
    return_text += ('<tr><th>CHB</th><td>'+'</td><td>'.join([str(entry.CHB_AC),str(entry.CHB_AN)])+'</td><td id="CHB_AF">'+str(entry.CHB_AF)+'</td></tr>')
    return_text += ('<tr><th>CHS (1KGP)</th><td>'+'</td><td>'.join([str(entry.CHS_1KGP_AC),str(entry.CHS_1KGP_AN)])+'</td><td id="CHS1KGP_AF">'+str(entry.CHS_1KGP_AF)+'</td></tr>')
    return_text += ('<tr><th>CDX</th><td>'+'</td><td>'.join([str(entry.CDX_AC),str(entry.CDX_AN)])+'</td><td id="CDX_AF">'+str(entry.CDX_AF)+'</td></tr>')
    return_text += ('<tr><th>CHN</th><td>'+'</td><td>'.join([str(entry.CHN_AC),str(entry.CHN_AN)])+'</td><td id="CHN_AF">'+str(entry.CHN_AF)+'</td></tr>')
    return_text += ('<tr><th>CHS</th><td>'+'</td><td>'.join([str(entry.CHS_AC),str(entry.CHS_AN)])+'</td><td id="CHS_AF">'+str(entry.CHS_AF)+'</td></tr>')
    return_text += ('<tr><th>JPT</th><td>'+'</td><td>'.join([str(entry.JPT_AC),str(entry.JPT_AN)])+'</td><td id="JPT_AF">'+str(entry.JPT_AF)+'</td></tr>')
    return_text += ('<tr><th>KHV</th><td>'+'</td><td>'.join([str(entry.KHV_AC),str(entry.KHV_AN)])+'</td><td id="KHV_AF">'+str(entry.KHV_AF)+'</td></tr>')
    return_text += '</tbody></table>'
    return HttpResponse(return_text)


         



