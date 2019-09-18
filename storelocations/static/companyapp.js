function Selecting(){

  var select=document.getElementById('updateSave');
  if (select.options[select.selectedIndex].value=='save'){
    document.getElementById('id_company_info_id').setAttribute("disabled", "");
  document.getElementById('GetCompanyData').setAttribute("disabled", "");
  document.getElementById('submitbtn').value='Save Company'
  return select.options[select.selectedIndex].value
  }
  else if (select.options[select.selectedIndex].value=='update') {
    document.getElementById('id_company_info_id').removeAttribute("disabled");
    document.getElementById('GetCompanyData').removeAttribute("disabled");
    document.getElementById('submitbtn').value='Update Company'


    return select.options[select.selectedIndex].value
  }
  else{
    alert('please select Save Or Update')
    return select.options[select.selectedIndex].value
  }

}
function searchCompanyId(){
  let slectobj=Selecting()
  if (slectobj=='update'){
  var info_id=document.getElementById('id_company_info_id').value;
  let request=new XMLHttpRequest()
  let req=request.open("get","http://"+localStorage.getItem('ip')+":7000/pushcompany/?id="+info_id)
  request.onreadystatechange=function () {
      if(this.status==200 && this.readyState==4 ){
          var status=JSON.parse(this.responseText)
          var ids=['id_company_name','id_company_size','id_company_contact','id_hq_locations_location','id_industry','id_estd_year','id_company_unique_id','id_hq_company_address_line1','id_hq_company_address_line2'];
          for(let i=0;i<=ids.length-1;i++){
            document.getElementById(ids[i]).value=status[ids[i].replace("id_", "")]
          }
          return false
      }
      else if(this.status>=500 && this.status<=550 && this.readyState==4){
        alert("Something went Wrong Try again.........")
        document.getElementById('id_company_name').value='';
        document.getElementById('id_company_website').value='';
        document.getElementById('id_company_size').value='';
        return false
      }
    else if(this.status>=400 && this.status<=499 && this.readyState==4){
      alert("info_id DoesNotExist")
      document.getElementById('id_company_name').value='';
      document.getElementById('id_company_website').value='';
      document.getElementById('id_company_size').value='';
      return false
    }
  }
  request.send()
}
}
function updateCompanyID(){
  let slectobj=Selecting()
  if (slectobj=='update'){
  var info_id=document.getElementById('id_company_info_id').value;
  var body={}
  var ids=["id_company_name",'id_company_info_id','id_company_size','id_company_contact','id_hq_locations_location','id_industry','id_estd_year','id_company_unique_id','id_hq_company_address_line1','id_hq_company_address_line2'];
  for(let i=0;i<=ids.length-1;i++){
    body[ids[i].replace('id_','')]=document.getElementById(ids[i]).value
  }
  let request=new XMLHttpRequest()
  let req=request.open("PUT","http://"+localStorage.getItem('ip')+":7000/pushcompany/")
  request.onreadystatechange=function () {
      if(this.status>=200 && this.status<=250 && this.readyState==4 ){
          alert('Company Updated Succsesfully')
  }
}
  request.send(JSON.stringify(body))
  return false
}
}
function filterFunction() {
  var span=document.getElementById('adding')
  span.innerHTML=''
  var input, filter, ul, li, a, i;
  input = document.getElementById("serach_id_industry");
  body= {"industry__icontains":input.value}
  let request=new XMLHttpRequest()
  let req=request.open("GET","http://"+localStorage.getItem('ip')+":7000/getIndustries/?industry__icontains="+input.value)
  request.onreadystatechange=function () {
      if(this.status>=200 && this.status<=250 && this.readyState==4 ){
          data=JSON.parse(this.responseText)
          for(let i=0;i<=data.length-1;i++){
            span.innerHTML=span.innerHTML+"<a id="+data[i]['industry_id']+" onclick='return selectIndustry(this)'>"+data[i]['industry']+"</a><br>"
          }
  }
}
  request.send()
}
function emptyThelist(span){
  span.innerHTML=''
}
function selectIndustry(span){
  if (document.getElementById('show_id_industry').value==''){
    document.getElementById('show_id_industry').value=span.innerText.trim();
    document.getElementById('adding').innerHTML=''
    if (document.getElementById('id_industry').value==''){
      document.getElementById('id_industry').value=span.innerText.trim()

    }
  }
  else{
    if (document.getElementById('show_id_industry').value.split(',').indexOf(span.innerText.trim()) == -1){
    document.getElementById('show_id_industry').value=document.getElementById('show_id_industry').value+','+span.innerText.trim();
    if (document.getElementById('id_industry').value.split(',').indexOf(span.innerText.trim()) == -1){
    if (document.getElementById('id_industry').value!='0'){
      document.getElementById('id_industry').value=document.getElementById('id_industry').value+','+span.innerText.trim()

    }
  }
  }
  }
  document.getElementById('adding').innerHTML=''
}
function clearFields(){
  document.getElementById('show_id_industry').value='';
  document.getElementById('id_industry').value=''

}
