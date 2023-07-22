table_select_script = """  var rows = Array.from(document.querySelectorAll('tr'));

  var headers = rows.map(el => {li = el.querySelectorAll('th'); return li})
  .filter(el => el.length>0);
  var results = rows.map(el =>{li = el.querySelectorAll('td'); return li})
  .filter(el => el.length>1);
function fun(header,exp_map){



  var map = new Map()

  for(var index = 0; index < headers[0].length;index++){
    map.set(headers[0][index].textContent,index)
  }
  found = true;
  var keys =[ ...map.keys() ];
  var exp_header_keys = Object.keys(exp_map)

   for (var row of results){
              for (var item_index = 0; item_index < row.length; item_index++){
                  var found = true;

                  for(var [key,value] of Object.entries(exp_map)){
                    if (row[map.get(key)].innerText !== value){
                      found = false;
                              break;
                      }

                      if (found){
                          var cell= row[map.get(header)];
                        	var children = cell.children
                          if(children.length >0){
                              return children[0];
                          }else{
                          return cell;}
                      }
                  }
                	break;
              }
   }
}
return fun(arguments[0],arguments[1]);
"""

find_element_by_text_script = """

var element_list = Array.from(document.querySelectorAll('*')).filter(el => String(el.innerText).trim() === String(arguments[0]) || (el['value'] !== undefined && String(el.value).trim() === String(arguments[0])));

if(element_list.length > 0){
    var btns = element_list.filter(ele => ele.tagName === "BUTTON");
    var links = element_list.filter(ele => ele.tagName === "A");
    if(btns.length > 0){
        console.log(btns[0])
        return btns[0]
    }else if(links.length > 0){
        return links[0]
    }else{
        return element_list[0];
    }
}else{
    return null;
}
"""