# 3d-web

This folder is for tutorial of threejs

## Installation

```bash
# Install yarnw
yarn set version stable
yarn install 

# for vite
yarn create vite my-vue-app --template vue

yarn add -D vite # manual installation

# to run (3 methods)
yarn vite
npx vite
npm run devv

```

## Glosary

* **Mesh**

    Collection of vertices, edges, and faces that define the shape of a 3D object. Fundamental structure used to represent 3D models 

    Components of a 3D Mesh:

    * Vertices – Points in 3D space that define positions.
    * Edges – Lines connecting two vertices.
    * Faces (Polygons) – Flat surfaces enclosed by edges, typically triangles or quadrilaterals.
    * Normals – Vector that is perpendicular to the surface of a 3D object at a given point, it is used to define the direction of a surface for lighting and shading. 
    * UV Coordinates – Mapping coordinates used to apply textures to the mesh.

    Types of Mesh Representations:

    * Triangle Mesh: Uses only triangles (widely used in real-time graphics like gaming).
    * Quad Mesh: Uses quadrilateral faces (preferred in modeling and animation for smoother deformations).
    * Polygon Mesh: Can contain a mix of triangles, quads, or n-sided polygons.

* **Geometry**
    
    The mathematical definition of the shape. Geometry can exist without being a mesh, such as parametric shapes (e.g., a sphere defined by a formula).

* **Physics Engine**

    Software component that simulates real-world physics in a virtual environment. It calculates how objects move, collide, and interact based on physical laws like gravity, friction, and momentum.

    Main Functions of a Physics Engine:

    * Rigid Body Dynamics – Simulates solid objects that don’t deform (e.g., a bouncing ball).
    * Soft Body Dynamics – Simulates flexible or squishy objects (e.g., cloth, jelly).
    * Collision Detection – Detects when objects touch or overlap.
    * Gravity & Forces – Simulates the effect of gravity, wind, explosions, etc.
    * Ragdoll Physics – Used for realistic character movements (e.g., when a character falls).
    * Fluid & Particle Simulation – Simulates water, smoke, fire, or explosions

## External Link

* https://vite.dev/guide
* https://devhints.io/yarn
* https://www.youtube.com/watch?v=Q7AOvWpIVHU
* https://en.wikipedia.org/wiki/Polygon_mesh

## Credit to 3D model owner
"2025 Automobili Pininfarina B95" (https://skfb.ly/puqIr) by Outlaw Games™ is licensed under Creative Commons Attribution-NonCommercial (http://creativecommons.org/licenses/by-nc/4.0/).