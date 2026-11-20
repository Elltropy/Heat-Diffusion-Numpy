import numpy as np 
import plotly.graph_objects as go


def plot_surface_slider(
    X,
    Y,
    surface,
    zlim=None,
    cmin=None,
    cmax=None,
    colorscale="Picnic",
    title="Matrix Power Evolution",
    frame_duration=40,
    transition_duration=40,
):
    """
    surface[t] should be a 2D array representing K^t u0 reshaped as a grid.
    """

    if len(surface) == 0:
        raise ValueError("surface list is empty.")

    if zlim is None:
        max_abs = max(np.max(np.abs(S)) for S in surface)
        zlim = max_abs

    if cmin is None:
        cmin = -zlim

    if cmax is None:
        cmax = zlim

    fig = go.Figure(
        data=[
            go.Surface(
                x=X,
                y=Y,
                z=surface[0],
                colorscale=colorscale,
                cmin=cmin,
                cmax=cmax,
            )
        ],

        frames=[
            go.Frame(
                data=[
                    go.Surface(
                        x=X,
                        y=Y,
                        z=surface[t],
                        colorscale=colorscale,
                        cmin=cmin,
                        cmax=cmax,
                    )
                ],
                name=str(t)
            )
            for t in range(len(surface))
        ]
    )

    fig.update_layout(
        title=title,

        scene=dict(
            zaxis=dict(range=[-zlim, zlim])
        ),

        updatemenus=[
            dict(
                type="buttons",
                showactive=False,
                buttons=[
                    dict(
                        label="Play",
                        method="animate",
                        args=[
                            None,
                            dict(
                                frame=dict(
                                    duration=frame_duration,
                                    redraw=True
                                ),
                                transition=dict(
                                    duration=transition_duration,
                                    easing="linear"
                                ),
                                fromcurrent=True,
                                mode="immediate"
                            )
                        ]
                    ),
                    dict(
                        label="Pause",
                        method="animate",
                        args=[
                            [None],
                            dict(
                                frame=dict(
                                    duration=0,
                                    redraw=False
                                ),
                                transition=dict(
                                    duration=0
                                ),
                                mode="immediate"
                            )
                        ]
                    )
                ]
            )
        ],

        sliders=[
            dict(
                active=0,
                currentvalue=dict(prefix="K^"),
                steps=[
                    dict(
                        method="animate",
                        args=[
                            [str(t)],
                            dict(
                                mode="immediate",
                                frame=dict(
                                    duration=0,
                                    redraw=True
                                ),
                                transition=dict(
                                    duration=0
                                )
                            )
                        ],
                        label=str(t)
                    )
                    for t in range(len(surface))
                ]
            )
        ]
    )

    fig.show()