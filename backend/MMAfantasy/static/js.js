var h = document.body.innerHTML.replace(/\href="{%/gi, 'href="##').replace(/\%}"/gi, '##"');
const c = h.replace(/\{%|{{/gi, '<span class="hide">{%').replace(/\%}|}}/gi, "%}</span>").replace(/\href="##/gi, 'href="{%').replace(/\##"/gi, '%}"');
document.body.innerHTML = c;