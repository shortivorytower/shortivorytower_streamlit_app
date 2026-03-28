const main_app = window.parent.document;
main_app.defaultView.MathJax = {tex: {inlineMath: [['$', '$'], ['\\(', '\\)']]}, svg: {fontCache: 'global'}};
(function () {
    const script = main_app.createElement('script');
    script.type = 'text/javascript';
    script.async = true;
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_SVG';
    main_app.head.appendChild(script);
})();