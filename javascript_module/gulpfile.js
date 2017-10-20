var gulp = require('gulp');
var concat = require('gulp-concat');

gulp.task('default', function () {
    return gulp.src([
        './util/emacs5-compatibility-patches.js'
        , './util/encoder.js'
        , './util/uuid.js'
        , './util/zet.js'
        , './super-glu.js'
        , './util/serialization.js'
        , './util/socket.io.js'
        , './core/messaging.js'
        , './core/messaging-gateway.js'
        , './services/orchestration/heartbeat-service.js'
        , './reference-data.js'
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