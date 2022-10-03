# Contributing

Thank you so much for your interest in contributing. All types of contributions are encouraged and valued. All you need to do is read the guidelines before making any chances!

## Request Support/Feature or Report an Error
If you have a problem with the SDK or you want a well-thought-out feature, please open an issue and provide all the information regarding your problem or idea. You don't need to label your own issue, the code maintainers will handle this job. If it is a problem, we're going to solve it as soon as possible.

## Code Contribution
Before implementing your own solution or solving an issue, please read the following guidelines to have a better-looking and unified code:
* **Always follow PEP-8**. The codes without proper styling is not going to be merged.
* **Check your code with a linter before creating a pull request**. We're strongly recommending you to use a Python linter software to check your code before submitting it.
* **Provide meaningful and standardized commit messages**. We have no rush to think about commit messages, since the project collaborators are all individual people, we have to stay on a standardized system. Please only use `feat`, `refactor`, `fix`, `docs`, and `chore`.
* **Make lots of commits**! You don't need to worry about commit count of your pull request since we use squash and merge method. It is better to have more and meaningfully small commits instead of big breaking changes.
* **Check the code on your picocell device**. Do not forget that we are working on embedded devices. You may think that you've done a little change, but in the world of tiny things, the little changes can go giant! Run your code on a picocell, and report the outputs or status on your pull request.
* **Follow the commit message standards on pull requests' titles**. Clear titles as important as clear commits.
* **Provide necessary information on your pull request**. "Why did you do this change, is it a feature, or a bug-fix? How does it change the previous code? Do we need to refactor something else? What are the successful results?" Don't let us have questions in our minds. Provide a well-written documentation about your change.

## Creating a Service as Application
We encourage you to create your own applications to the services if they are not available built-in since the idea behind this project is to make easy connections on many services with using cellular. To follow this mission, we need to support more services.

A small and simple guide given to you, developers, [in this file](examples/__sdk__/create_your_own_method.py) about how to create your own application using state manager model.