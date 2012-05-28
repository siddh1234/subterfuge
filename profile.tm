<!--    HEADER      -->
    {% include "includes/header.inc" %}
<!--    END_HEADER  -->

<body>

    <!--        NAVBAR          -->
        {% include "includes/nav.inc" %}
    <!--        END_NAVBAR      -->
    
    
    <!--        SIDENAV         -->
        {% include "includes/sidenav.inc" %}
    <!--        END_SIDENAV     -->
    
    <!--        MAIN_CONTENT    -->
    
<div id="main">
    {% block content %}{% endblock %}
</div>



    <!--        MAIN_CONTENT    -->
</body>
</html>