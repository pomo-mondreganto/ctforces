module.exports = {
    parser: 'babel-eslint',
    env: {
        browser: true,
        es6: true
    },
    extends: ['eslint:recommended', 'plugin:react/recommended', 'airbnb-base'],
    globals: {
        Atomics: 'readonly',
        SharedArrayBuffer: 'readonly'
    },
    parserOptions: {
        ecmaFeatures: {
            jsx: true
        },
        ecmaVersion: 2018,
        sourceType: 'module'
    },
    plugins: ['react'],
    rules: {
        indent: ['error', 4],
        'linebreak-style': ['error', 'unix'],
        quotes: ['error', 'single'],
        semi: ['error', 'always'],
        "import/no-extraneous-dependencies": ["error", { "devDependencies": true }],
        "react/prop-types": [0], //remove it later
        "no-await-in-loop": [0],
        "no-continue": [0]
    },
    settings: {
        react: {
            createClass: 'createReactClass',
            pragma: 'React',
            version: 'detect'
        }
    }
};
