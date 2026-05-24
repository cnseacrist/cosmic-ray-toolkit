# Cosmic Ray Toolkit

This repo is for building out some of the basic calculations and computational physics to model a cosmic ray cascade in earth's atmosphere.

## Description

The project will include a simplified framework called the Heitler Toy Model to build out some of the basic intuition of the cosmic ray cascade process and deliver some of the fundamental physical takeaways that still hold true for some of the most modern iterations of cosmic ray cascade calculations. 

That intuition will be extended to the more complex models like the Gaisser-Hillas function - a model that more thoroughly details the particle interactions in a cosmic ray cascade. Monte Carlo methods will be employed to simulate many different cascades and compare those results to open-source cosmic ray data, like that from the Pierre-Auger Obervatory in Argentina.

This project will include a implementation of the Standard Atmosphere calculation in which the cascades will occur, and then finally an analysis of the open source data from Pierre-Auger. 

## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

The program requirments can be found in requirements.txt and include:
 - numpy
 - scipy
 - matplotlib
 - pandas
 - jupyter

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets

The repo includes 5 projects:
 - Heitler Cascade Simulator
 - Gaisser-Hillas Profile Fitter
 - Atmospheric Depth Calculator
 - Cascade in a Realistic Atmosphere
 - Auger Open Data Analysis

### Project 1 - The Heitler Cascade Simulator
This program calculates the number of particles produced in the simplified Heitler model of an EM cascade of cosmic rays. It outputs a plot of how the number of particles produced varies with atmospheric depth for a few different selected energies. 

In the example figure, this was done for primary particle energies of 10^4, 10^6 and 10^8 MeV.

![Number of Particles vs. Atmospheric Depth](figures/heitler_cascade.png)

```
code blocks for commands
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46)
