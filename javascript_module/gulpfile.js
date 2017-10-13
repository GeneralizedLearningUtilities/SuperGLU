var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('default', function () {
    return gulp.src([
        // './util/zet.js'
        // // , '!./util/zet.js'              //Ignore from ./util/*.js mentioned below
        // , '!./util/socket.io.js'        //ignore
        // , '!./services/storage/*.js'    //ignore
        // , '!./services/authentication/*.js'      //ignore
        //
        // , './util/*.js'
        // , './core/*.js'
        // , './services/authentication/*.js', './services/logging/*.js', './services/orchestration/*.js'
        // , './services/storage/*.js'
        // , './services/studentmodel/*.js'
        // , './reference-data.js'
        // , './super-glu.js'

        './util/emacs5-compatibility-patches.js'
        , './util/encoder.js'
        , './util/uuid.js'
        , './util/zet.js'
        , './super-glu.js'
        , './util/serialization.js'
        , './core/messaging.js'
        , './core/messaging-gateway.js'
        , './services/orchestration/heartbeat-service.js'
        , './reference-data.js'

        // <!-- General Utilities Imports -->
        // <!--<script type="text/javascript" src="js/Util/emacs5-compatibility-patches.js"></script>-->
        // <!--<script type="text/javascript" src="js/Util/encoder.js"></script>-->
        //
        // <!--&lt;!&ndash; SuperGLU Imports &ndash;&gt;-->
        // <!--<script type="text/javascript" src="js/Util/uuid.js"></script>-->
        // <!--<script type="text/javascript" src="js/Util/zet.js"></script>-->
        // <!--<script type="text/javascript" src="js/super-glu.js"></script>-->
        // <!--<script type="text/javascript" src="js/Util/serialization.js"></script>-->
        // <!--<script type="text/javascript" src="js/Core/messaging.js"></script>-->
        // <!--<script type="text/javascript" src="js/Core/messaging-gateway.js"></script>-->
        //
        // <!--&lt;!&ndash; SuperGLU Services &ndash;&gt;-->
        // <!--<script type="text/javascript" src="js/Services/Orchestration/heartbeat-service.js"></script>-->
        //
        // <!--&lt;!&ndash; Reference-Implementation Data &ndash;&gt;-->
        // <!--<script type="text/javascript" src="js/reference-data.js"></script>-->
    ])
        .pipe(concat('superglu-all.js'))
        .pipe(gulp.dest('./dist/'));
});

gulp.task('watch', ['default'], function () {
    gulp.watch('./core/*.js', ['default']);
    gulp.watch('./services/**/*.js', ['default']);
    gulp.watch('./util/*.js', ['default']);
    gulp.watch('./*.js', ['default']);
});