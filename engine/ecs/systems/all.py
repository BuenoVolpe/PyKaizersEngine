from game.ecs.signals.all import PlayerSignals
from engine.ecs.systems.render import RenderSystem, CameraSystem
from engine.ecs.systems.visual.animation import SimpleAnimationSystem, StateAnimationSystem
from engine.ecs.systems.visual.rotate import LookAtSystem, VisualRotationSystem
from engine.ecs.systems.movement import MovementSystem, AngularMovementSystem
from engine.ecs.systems.inputs import InputSystem