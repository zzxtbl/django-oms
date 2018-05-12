
/* Highlight */
$( document ).ready(function() {
    hljs.initHighlightingOnLoad();
    $('table').addClass('table table-striped table-hover');
});


$('body').scrollspy({
    target: '.bs-sidebar',
});


/* Prevent disabled links from causing a page reload */
$("li.disabled a").click(function() {
    event.preventDefault();
});

// 给markdown图片添加链接
$(document).ready(function() {
    var n = 1;
    $("p img").each(function() {
        n++;   // 让图片独立
        var strA = "<a href='" + this.src + "' data-lightbox='xxoo-" + n + "' data-title='" + this.alt + "'></a>";
        $(this).wrapAll(strA);
    });
});
