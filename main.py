from typing import List, Tuple
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation


class ParticleSimulation:
    def __init__(
        self,
        initial_conditions: List[float],
        mass_particle: float,
        time_span: Tuple[float, float],
        num_frames: int,
    ):
        self.initial_conditions = initial_conditions
        self.mass_particle = mass_particle
        self.time_span = time_span
        self.num_frames = num_frames

    def calculate_interaction_force(self, t: float, y: List[float]) -> List[float]:
        g: float = 9.8  # Aceleración debida a la gravedad (m/s^2)

        x, y, vx, vy = y

        # Fuerza gravitatoria en la partícula
        fx: float = 0.0
        fy: float = -self.mass_particle * g

        return [vx, vy, fx, fy]

    def simulate(self):
        time_points: np.ndarray = np.linspace(
            self.time_span[0], self.time_span[1], self.num_frames
        )

        # Resolver las ecuaciones diferenciales utilizando solve_ivp
        solution: solve_ivp = solve_ivp(
            self.calculate_interaction_force,
            self.time_span,
            self.initial_conditions,
            t_eval=time_points,
        )

        return solution

    def animate(self, solution: solve_ivp):
        # Configurar la gráfica
        fig, ax = plt.subplots(figsize=(10, 8))
        ax.set_xlim(min(solution.y[0]), max(solution.y[0]))
        ax.set_ylim(0, max(solution.y[1]) + 2)
        ax.set_title(
            "Simulación de Movimiento de Partícula Utilizando las Leyes de Newton"
        )
        ax.set_xlabel("Distancia (m)")
        ax.set_ylabel("Altura (m)")

        # Inicializar la partícula
        (particle,) = ax.plot([], [], "bo", markersize=10, label="Partícula")
        (trajectory,) = ax.plot([], [], "b--", label="Trayectoria")

        # Información en tiempo real
        text_info = ax.text(0.02, 0.95, "", transform=ax.transAxes)

        def update(frame: int) -> Tuple[plt.Line2D, plt.Line2D, plt.Text]:
            particle.set_data(solution.y[0, frame], solution.y[1, frame])
            trajectory.set_data(solution.y[0, :frame], solution.y[1, :frame])

            # Actualizar la información en tiempo real
            info: str = f"Tiempo: {solution.t[frame]:.2f} s\nPosición: ({solution.y[1, frame]:.2f} m, {solution.y[0, frame]:.2f} m)\nVelocidad: ({solution.y[2, frame]:.2f} m/s, {solution.y[3, frame]:.2f} m/s)"
            text_info.set_text(info)

            return particle, trajectory, text_info

        # Anima la gráfica
        ani: FuncAnimation = FuncAnimation(
            fig, update, frames=self.num_frames, interval=50, blit=True
        )

        plt.legend()
        plt.grid(True)
        plt.show()


# Condiciones iniciales [x, y, vx, vy]
initial_conditions: List[float] = [0.0, 0.0, 5.0, 10.0]

# Masa de la partícula (experimenta con diferentes masas)
mass_particle: float = 1.0

# Intervalo de tiempo y número de frames (experimenta con diferentes valores)
time_span: Tuple[float, float] = (0, 2)
num_frames: int = 100

# Crear una instancia de la simulación
particle_sim = ParticleSimulation(
    initial_conditions, mass_particle, time_span, num_frames
)

# Realizar la simulación
solution = particle_sim.simulate()

# Visualizar la animación
particle_sim.animate(solution)
