const path = require("path");
const {spawn} = require('child_process');

const gulp = require('gulp');
const clean = require('gulp-clean');
const Promise = require('bluebird');
const zip = require('gulp-zip');

const output_dir = 'build/';

// const support_files = [
//     // DO NOT INCLUDE ANY OF THE FOLLOWING: 'examples', 'samples'

//     // Assignment files
//     'solution/!(_)*.py',  // ignore files with leading _
//     //'solution/images/**/*',
//     'solution/images/*',  // top-level only for now

//     // Modules (1st & 3rd party)
//     'solution/modules/**/*',

//     // Linting
//     'solution/pylintrc'

// ];

// var exec = require('child_process').exec;

// gulp.task('test:build', function (cb) {
//   exec('cd build && unzip -o a3_files.zip -d a3_files_test/ && cd a3_files_test && cp ../../solution/_sample_task1_1.py . && python3 _sample_task1_1.py', function (err, stdout, stderr) {
//     console.log(stdout);
//     console.log(stderr);
//     cb(err);
//   });
// })

// let promise = function (files, from_dir, to_dir, zip_name, sub_dir) {
//     const tmp_dir = to_dir + zip_name + "_tmp/";

//     if (typeof sub_dir === 'undefined') {
//         sub_dir = '';
//     }

//     return new Promise((resolve, reject) => {
//         return gulp.src(files, {base: from_dir})
//             .pipe(gulp.dest(tmp_dir + sub_dir))
//             .on('error', reject)
//             .on('end', resolve);
//     })
// };

// let bundle = function (promises, to_dir, zip_name) {
//     const tmp_dir = to_dir + zip_name + "_tmp/";

//     return Promise.all(promises)
//         .then(() => {
//             gulp.src(tmp_dir + '**/*', {base: tmp_dir})
//                 .pipe(zip(zip_name + '.zip'))
//                 .pipe(gulp.dest(to_dir));
//         });
// };

// gulp.task('build', ['clean:build'], function () {
//     const zip_name = 'a3_files';

//     const files = [
//         // TODO: this
//         // Assignment template
//         // 'dots/a3.py',
//         //
//         // // Spec
//         // 'assignment3.html',
//         //
//         // // Misc.
//         // 'LICENSE'
//     ];

//     return bundle([
//         promise(support_files, 'solution/', output_dir, zip_name)
//     ], output_dir, zip_name).then(() => {

//         return Promise.all([
//             // gulp.src(['solution/a3.py'], {base: 'solution/'}).pipe(gulp.dest(output_dir)),
//             gulp.src(['spec/dist/**/*']).pipe(gulp.dest(path.join(output_dir, 'spec/')))
//         ]);
//     })
// });

// gulp.task('mark', function () {
//     const zip_name = '2017s1a3_marking';
//
//     let files = [
//         // Thrall configuration
//         'a3.thrall',
//
//         // Assignment 3 Schema
//         'schema-a3.js'
//     ];
//
//     return bundle([
//         promise(files, './', output_dir, zip_name),
//         promise('', './', output_dir, zip_name, 'assignments'),
//         promise(support_files, 'dots/', output_dir, zip_name, 'assets')
//     ], output_dir, zip_name);
// });

// gulp.task('solution', function () {
//     const zip_name = 'a3_solution';

//     return bundle([
//         promise('solution.py', './', output_dir, zip_name)
//     ], output_dir, zip_name);
// });

gulp.task('clean:tmp', function () {
    return gulp.src(output_dir + "*_tmp/")
        .pipe(clean());
});

gulp.task('clean:build', function () {
    return gulp.src(output_dir)
        .pipe(clean());
});

gulp.task('clean:spec', function () {
    return gulp.src("spec/dist/")
        .pipe(clean());
});

gulp.task('clean', ['clean:build', 'clean:spec']);

function simpleGulpError(cb) {
    return (code) => {
        code = parseInt(code.toString(), 10);
        if (code === 0) {
            cb(null);
        } else {
            const error = new Error(`Exited with code: ${code}`);
            error.showStack = false;
            cb(error);
        }
    };
}

// was used to ignore a3 template from linting
// but is not needed due to no template provided for 2018s2a3
const TEMPLATE_PATTERN = "nah_boi";

gulp.task("pylint:prod", (cb) => {

    const proc = spawn("find", [".", "-iname", "*.py", "-not", "-iname", TEMPLATE_PATTERN, "-not", "-iname", "_*", "-exec", "python3", "-m", "pylint", "--rcfile=pylintrc", "{}", "+"], {stdio: 'inherit', cwd:'solution'});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task("pylint:dev", (cb) => {

    const proc = spawn("find", [".", "-iname", "*.py", "-not", "-iname", TEMPLATE_PATTERN, "-exec", "python3", "-m", "pylint", "--rcfile=pylintrc", "--disable=missing-docstring,fixme", "{}", "+"], {stdio: 'inherit', cwd: 'solution'});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task("pylint:template", (cb) => {

    const proc = spawn("find", [".", "-iname", TEMPLATE_PATTERN, "-exec", "python3", "-m", "pylint", "--rcfile=pylintrc", "--disable=missing-docstring,fixme,unused-variable", "{}", "+"], {stdio: 'inherit', cwd: 'solution'});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task("pylint:template:prod", (cb) => {

    const proc = spawn("find", [".", "-iname", TEMPLATE_PATTERN, "-exec", "python3", "-m", "pylint", "--rcfile=pylintrc", "{}", "+"], {stdio: 'inherit', cwd: 'solution'});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task('pylint', ['pylint:prod']);

gulp.task("spec:build", ['clean:spec'], (cb) => {
    const proc = spawn("npm", ["run", "production"], {cwd: "spec", stdio: "inherit"});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task("spec:pdf", (cb) => {
    const proc = spawn("npm", ["run", "pdf"], {cwd: "spec", stdio: "inherit"});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task("spec:dev", (cb) => {
    const proc = spawn("npm", ["run", "start"], {cwd: "spec", stdio: "inherit"});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task('spec', ['clean:spec', 'spec:build']);

gulp.task("analyse:dead", (cb) => {
    const proc = spawn("find", ["dots", "-iname", "*.py", "-exec", "python3", "-m", "vulture", "{}", "+"], {stdio: 'inherit'});

    proc.on('exit', simpleGulpError(cb));
});

gulp.task('default', ['build']);