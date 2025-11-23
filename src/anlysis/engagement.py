import pandas as pd

from plotly import express as px
from plotly import graph_objects as go
from src.cleaning.video_cleaning import clean_video_df

def authors_videos(df):
    """Analisis author dengan video terbanyak dan tersedikit."""
    # ==================Top & Bottom Authors by Video Count==================
    all_authors = df['authorMeta.name'].value_counts()
    mean_value = all_authors.mean()

    top_authors = all_authors.head(5)
    bottom_authors = all_authors.tail(5)

    vid_authors = go.Figure()

    # 1
    vid_authors.add_trace(go.Bar(
        x=top_authors.index,
        y=top_authors.values,
        name='Total Videos',
        marker_color='midnightblue',
        visible=True
    ))
    # 2
    vid_authors.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(dash='dash', color='orange'),
        name=f"Mean ({mean_value:.2f})",
        showlegend=True,
        visible=True
    ))

    # 3
    vid_authors.add_trace(go.Bar(
        x=bottom_authors.index,
        y=bottom_authors.values,
        name='Total Videos',
        marker_color='midnightblue',
        visible=False
    ))

    # 4
    vid_authors.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(dash='dash', color='orange'),
        name=f"Mean ({mean_value:.2f})",
        showlegend=True,
        visible=False
    ))

    # --- Garis mean full chart ---
    vid_authors.add_hline(
        y=mean_value,
        line_dash="dash",
        line_color="orange",
    )

    # --- Dropdown ---
    vid_authors.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list([
                    dict(
                        label="Top 5 Authors",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False]},
                            {"title": "Top 5 Authors with Most Videos"}
                        ]
                    ),
                    dict(
                        label="Bottom 5 Authors",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True]},
                            {"title": "Bottom 5 Authors with Least Videos"}
                        ]
                    )
                ]),
                direction="down",
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0,
                xanchor="left",
                y=1.2,
                yanchor="top"
            ),
        ]
    )

    vid_authors.update_layout(
        title={
            "text": "Top 5 Authors with Most Videos",
            "x": 0.5,             # center
            "xanchor": "center"
        },
        xaxis_title="Author Name",
        yaxis_title="Videos",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        )
    )

    return vid_authors

def likes_analysis(df):
    """Analisis video dengan likes tertinggi dan terendah."""
    # =================Top & Bottom Videos by Likes==================
    # Top 5 likes
    top_likes = (df.nlargest(5, 'diggCount')[['authorMeta.name', 'diggCount']].sort_values(by='diggCount', ascending=False))
    top_likes['video_label'] = top_likes['authorMeta.name'] + ' - Vid ' + (top_likes.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Bottom 5 likes
    bottom_likes = (df.nsmallest(5, 'diggCount')[['authorMeta.name', 'diggCount']].sort_values(by='diggCount', ascending=False))
    bottom_likes['video_label'] = bottom_likes['authorMeta.name'] + ' - Vid ' + (bottom_likes.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Mean
    mean_likes = df['diggCount'].mean()
    fig_likes = go.Figure()

    # 1
    fig_likes.add_trace(go.Bar(
        x=top_likes['video_label'],
        y=top_likes['diggCount'],
        name="Top 5 Videos",
        marker_color="midnightblue",
        visible=True,
        text=None
    ))

    # 2
    fig_likes.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean Likes ({mean_likes:.2f})",
        showlegend=True,
        visible=True
    ))

    # 3
    fig_likes.add_trace(go.Bar(
        x=bottom_likes['video_label'],
        y=bottom_likes['diggCount'],
        name="Bottom 5 Videos",
        marker_color="midnightblue",
        visible=False,
        text=bottom_likes['diggCount'],          
        textposition='outside'                   
    ))

    # 4
    fig_likes.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean Likes ({mean_likes:.2f})",
        showlegend=True,
        visible=False
    ))

    # ADD HLINE MEAN
    fig_likes.add_hline(
        y=mean_likes,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Mean = {mean_likes:.2f}",
        annotation_position="top right"
    )


    # DROPDOWN MENU
    fig_likes.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Top 5 Videos",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False]},
                            {"title": "Top 5 Videos with Highest Likes"}
                        ]
                    ),
                    dict(
                        label="Bottom 5 Videos",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True]},
                            {"title": "Bottom 5 Videos with Lowest Likes"}
                        ]
                    ),
                ],
                direction="down",
                showactive=True,
                x=0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
    )

    #   LAYOUT / TITLES
    fig_likes.update_layout(
        title=dict(
            text="Top 5 Videos with Highest Likes",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Video Label",
        yaxis_title="Likes",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        )
    )

    return fig_likes

def comment_analysis(df):
    """Analisis video dengan comment tertinggi dan terendah."""
    # =================Top & Bottom Videos by Comments==================
    # Top 5 comment
    top_comment = (df.nlargest(5, 'commentCount')[['authorMeta.name', 'commentCount']].sort_values(by='commentCount', ascending=False))
    top_comment['video_label'] = top_comment['authorMeta.name'] + ' - Vid ' + (top_comment.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Bottom 5 comment
    bottom_comment = (df.nsmallest(5, 'commentCount')[['authorMeta.name', 'commentCount']].sort_values(by='commentCount', ascending=False))
    bottom_comment['video_label'] = bottom_comment['authorMeta.name'] + ' - Vid ' + (bottom_comment.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Mean
    mean_comment = df['commentCount'].mean()

    fig_comment = go.Figure()

    # 1
    fig_comment.add_trace(go.Bar(
        x=top_comment['video_label'],
        y=top_comment['commentCount'],
        name="Top 5 Videos",
        marker_color="midnightblue",
        visible=True,
        text=None
    ))

    # 2
    fig_comment.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean comment ({mean_comment:.2f})",
        showlegend=True,
        visible=True
    ))

    # 3
    fig_comment.add_trace(go.Bar(
        x=bottom_comment['video_label'],
        y=bottom_comment['commentCount'],
        name="Bottom 5 Videos",
        marker_color="midnightblue",
        visible=False,
        text=bottom_comment['commentCount'],          
        textposition='outside'                   
    ))

    # 4
    fig_comment.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean comment ({mean_comment:.2f})",
        showlegend=True,
        visible=False
    ))

    # ADD HLINE MEAN
    fig_comment.add_hline(
        y=mean_comment,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Mean = {mean_comment:.2f}",
        annotation_position="top right"
    )


    # DROPDOWN MENU
    fig_comment.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Top 5 Videos",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False]},
                            {"title": "Top 5 Videos with Highest comment"}
                        ]
                    ),
                    dict(
                        label="Bottom 5 Videos",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True]},
                            {"title": "Bottom 5 Videos with Lowest comment"}
                        ]
                    ),
                ],
                direction="down",
                showactive=True,
                x=0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
    )

    #   LAYOUT / TITLES
    fig_comment.update_layout(
        title=dict(
            text="Top 5 Videos with Highest comment",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Video Label",
        yaxis_title="Comments",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        )
    )

    return fig_comment

def share_analysis(df):
    """Analisis video dengan share tertinggi dan terendah."""
    # =================Top & Bottom Videos by Shares==================
    # Top 5 shares
    top_shares = (df.nlargest(5, 'shareCount')[['authorMeta.name', 'shareCount']].sort_values(by='shareCount', ascending=False))
    top_shares['video_label'] = top_shares['authorMeta.name'] + ' - Vid ' + (top_shares.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Bottom 5 shares
    bottom_shares = (df.nsmallest(5, 'shareCount')[['authorMeta.name', 'shareCount']].sort_values(by='shareCount', ascending=False))
    bottom_shares['video_label'] = bottom_shares['authorMeta.name'] + ' - Vid ' + (bottom_shares.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Mean
    mean_shares = df['shareCount'].mean()

    fig_shares = go.Figure()

    # 1
    fig_shares.add_trace(go.Bar(
        x=top_shares['video_label'],
        y=top_shares['shareCount'],
        name="Top 5 Videos",
        marker_color="midnightblue",
        visible=True,
        text=None
    ))

    # 2
    fig_shares.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean shares ({mean_shares:.2f})",
        showlegend=True,
        visible=True
    ))

    # 3
    fig_shares.add_trace(go.Bar(
        x=bottom_shares['video_label'],
        y=bottom_shares['shareCount'],
        name="Bottom 5 Videos",
        marker_color="midnightblue",
        visible=False,
        text=bottom_shares['shareCount'],          
        textposition='outside'                   
    ))

    # 4
    fig_shares.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean shares ({mean_shares:.2f})",
        showlegend=True,
        visible=False
    ))

    # ADD HLINE MEAN
    fig_shares.add_hline(
        y=mean_shares,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Mean = {mean_shares:.2f}",
        annotation_position="top right"
    )

    # DROPDOWN MENU
    fig_shares.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Top 5 Videos",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False]},
                            {"title": "Top 5 Videos with Highest shares"}
                        ]
                    ),
                    dict(
                        label="Bottom 5 Videos",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True]},
                            {"title": "Bottom 5 Videos with Lowest shares"}
                        ]
                    ),
                ],
                direction="down",
                showactive=True,
                x=0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
    )

    #   LAYOUT / TITLES
    fig_shares.update_layout(
        title=dict(
            text="Top 5 Videos with Highest shares",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Video Label",
        yaxis_title="Shares",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        )
    )

    return fig_shares

def saved_analysis(df):
    """Analisis video dengan saved tertinggi dan terendah."""
    # =================Top & Bottom Videos by Saved==================
    # Top 5 saved
    top_saved = (df.nlargest(5, 'collectCount')[['authorMeta.name', 'collectCount']].sort_values(by='collectCount', ascending=False))
    top_saved['video_label'] = top_saved['authorMeta.name'] + ' - Vid ' + (top_saved.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Bottom 5 saved
    bottom_saved = (df.nsmallest(5, 'collectCount')[['authorMeta.name', 'collectCount']].sort_values(by='collectCount', ascending=False))
    bottom_saved['video_label'] = bottom_saved['authorMeta.name'] + ' - Vid ' + (bottom_saved.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Mean
    mean_saved = df['collectCount'].mean()

    fig_saved = go.Figure()

    # 1
    fig_saved.add_trace(go.Bar(
        x=top_saved['video_label'],
        y=top_saved['collectCount'],
        name="Top 5 Videos",
        marker_color="midnightblue",
        visible=True,
        text=None
    ))

    # 2
    fig_saved.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean saved ({mean_saved:.2f})",
        showlegend=True,
        visible=True
    ))

    # 3
    fig_saved.add_trace(go.Bar(
        x=bottom_saved['video_label'],
        y=bottom_saved['collectCount'],
        name="Bottom 5 Videos",
        marker_color="midnightblue",
        visible=False,
        text=bottom_saved['collectCount'],          
        textposition='outside'                   
    ))

    # 4
    fig_saved.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean saved ({mean_saved:.2f})",
        showlegend=True,
        visible=False
    ))

    # ADD HLINE MEAN
    fig_saved.add_hline(
        y=mean_saved,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Mean = {mean_saved:.2f}",
        annotation_position="top right"
    )

    # DROPDOWN MENU
    fig_saved.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Top 5 Videos",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False]},
                            {"title": "Top 5 Videos with Highest saved"}
                        ]
                    ),
                    dict(
                        label="Bottom 5 Videos",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True]},
                            {"title": "Bottom 5 Videos with Lowest saved"}
                        ]
                    ),
                ],
                direction="down",
                showactive=True,
                x=0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
    )

    #   LAYOUT / TITLES
    fig_saved.update_layout(
        title=dict(
            text="Top 5 Videos with Highest saved",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Video Label",
        yaxis_title="Saved",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        )
    )

    return fig_saved

def views_analysis(df):
    """Analisis video dengan views tertinggi dan terendah."""
    # =================Top & Bottom Videos by Views==================
    # Top 5 views
    top_views = (df.nlargest(5, 'playCount')[['authorMeta.name', 'playCount']].sort_values(by='playCount', ascending=False))
    top_views['video_label'] = top_views['authorMeta.name'] + ' - Vid ' + (top_views.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Bottom 5 views
    bottom_views = (df.nsmallest(5, 'playCount')[['authorMeta.name', 'playCount']].sort_values(by='playCount', ascending=False))
    bottom_views['video_label'] = bottom_views['authorMeta.name'] + ' - Vid ' + (bottom_views.groupby('authorMeta.name').cumcount() + 1).astype(str)
    # Mean
    mean_views = df['playCount'].mean()

    fig_views = go.Figure()

    # 1
    fig_views.add_trace(go.Bar(
        x=top_views['video_label'],
        y=top_views['playCount'],
        name="Top 5 Videos",
        marker_color="midnightblue",
        visible=True,
        text=None
    ))

    # 2
    fig_views.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean views ({mean_views:.2f})",
        showlegend=True,
        visible=True
    ))

    # 3
    fig_views.add_trace(go.Bar(
        x=bottom_views['video_label'],
        y=bottom_views['playCount'],
        name="Bottom 5 Videos",
        marker_color="midnightblue",
        visible=False,
        text=bottom_views['playCount'],          
        textposition='outside'                   
    ))

    # 4
    fig_views.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean views ({mean_views:.2f})",
        showlegend=True,
        visible=False
    ))

    # ADD HLINE MEAN
    fig_views.add_hline(
        y=mean_views,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Mean = {mean_views:.2f}",
        annotation_position="top right"
    )


    # DROPDOWN MENU
    fig_views.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Top 5 Videos",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False]},
                            {"title": "Top 5 Videos with Highest views"}
                        ]
                    ),
                    dict(
                        label="Bottom 5 Videos",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True]},
                            {"title": "Bottom 5 Videos with Lowest views"}
                        ]
                    ),
                ],
                direction="down",
                showactive=True,
                x=0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
    )

    #   LAYOUT / TITLES
    fig_views.update_layout(
        title=dict(
            text="Top 5 Videos with Highest views",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Video Label",
        yaxis_title="Views",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        )
    )

    return fig_views

def duration_analysis(df):
    """Analisis video dengan duration tertinggi dan terendah."""
    # =================Top & Bottom Videos by Duration==================
    # Top 5 duration
    top_duration = (df.nlargest(5, 'videoMeta.duration')[['authorMeta.name', 'videoMeta.duration']].sort_values(by='videoMeta.duration', ascending=False))
    top_duration['video_label'] = top_duration['authorMeta.name'] + ' - Vid ' + (top_duration.groupby('authorMeta.name').cumcount() + 1).astype(str)

    # Bottom 5 duration
    bottom_duration = (df.nsmallest(5, 'videoMeta.duration')[['authorMeta.name', 'videoMeta.duration']].sort_values(by='videoMeta.duration', ascending=False))
    bottom_duration['video_label'] = bottom_duration['authorMeta.name'] + ' - Vid ' + (bottom_duration.groupby('authorMeta.name').cumcount() + 1).astype(str)
    # Mean
    mean_duration = df['videoMeta.duration'].mean()

    fig_views = go.Figure()

    # 1
    fig_views.add_trace(go.Bar(
        x=top_duration['video_label'],
        y=top_duration['videoMeta.duration'],
        name="Top 5 Durations",
        marker_color="midnightblue",
        visible=True,
        text=None
    ))

    # 2
    fig_views.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean duration ({mean_duration:.2f})",
        showlegend=True,
        visible=True
    ))

    # 3
    fig_views.add_trace(go.Bar(
        x=bottom_duration['video_label'],
        y=bottom_duration['videoMeta.duration'],
        name="Bottom 5 Videos",
        marker_color="midnightblue",
        visible=False,
        text=bottom_duration['videoMeta.duration'],          
        textposition='outside'                   
    ))

    # 4
    fig_views.add_trace(go.Scatter(
        x=[None], y=[None],
        mode="lines",
        line=dict(color="orange", dash="dash"),
        name=f"Mean duration ({mean_duration:.2f})",
        showlegend=True,
        visible=False
    ))

    # ADD HLINE MEAN
    fig_views.add_hline(
        y=mean_duration,
        line_dash="dash",
        line_color="orange",
        annotation_text=f"Mean = {mean_duration:.2f}",
        annotation_position="top right"
    )

    # DROPDOWN MENU
    fig_views.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(
                        label="Top 5 Videos",
                        method="update",
                        args=[
                            {"visible": [True, True, False, False]},
                            {"title": "Top 5 Videos with Highest duration"}
                        ]
                    ),
                    dict(
                        label="Bottom 5 Videos",
                        method="update",
                        args=[
                            {"visible": [False, False, True, True]},
                            {"title": "Bottom 5 Videos with Lowest duration"}
                        ]
                    ),
                ],
                direction="down",
                showactive=True,
                x=0,
                xanchor="left",
                y=1.15,
                yanchor="top"
            )
        ]
    )

    #   LAYOUT / TITLES
    fig_views.update_layout(
        title=dict(
            text="Top 5 Videos with Highest duration",
            x=0.5,
            xanchor="center"
        ),
        xaxis_title="Video Label",
        yaxis_title="Duration (seconds)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="right",
            x=1
        )
    )

    return fig_views

def videos_over_time(df):
    """Analisis video yang dibuat dari waktu ke waktu."""
    # =================Line Chart of Videos Created Over Time==================
    # Line chart with dropdown menu for different time ranges
    df['createTimeISO'] = pd.to_datetime(df['createTimeISO'])

    latest_date = df['createTimeISO'].max()

    # Rentang waktu
    three_month = latest_date - pd.Timedelta(days=90)
    one_month = latest_date - pd.Timedelta(days=30)
    one_week  = latest_date - pd.Timedelta(days=7)
    one_day   = latest_date - pd.Timedelta(days=1)

    # Filter dataset
    data_all_day = df
    data_last_3month = df[df['createTimeISO'] >= three_month]
    data_last_month = df[df['createTimeISO'] >= one_month]
    data_last_week  = df[df['createTimeISO'] >= one_week]
    data_last_day   = df[df['createTimeISO'] >= one_day]

    # Resample harian
    daily_all = data_all_day.resample('D', on='createTimeISO').size().reset_index(name='Total')
    daily_3month = data_last_3month.resample('D', on='createTimeISO').size().reset_index(name='Total')
    daily_month = data_last_month.resample('D', on='createTimeISO').size().reset_index(name='Total')
    daily_week = data_last_week.resample('D', on='createTimeISO').size().reset_index(name='Total')
    daily_day  = data_last_day.resample('H', on='createTimeISO').size().reset_index(name='Total')

    # Mean
    mean_all_day  = daily_all['Total'].mean()
    mean_3month = daily_3month['Total'].mean()
    mean_month = daily_month['Total'].mean()
    mean_week = daily_week['Total'].mean()
    mean_day = daily_day['Total'].mean()

    # Plot
    fig_lines = go.Figure()

    # ALL TIME
    fig_lines.add_trace(go.Scatter(
        x=daily_all['createTimeISO'],
        y=daily_all['Total'],
        name='All Day',
        visible=True
    ))

    fig_lines.add_trace(go.Scatter(
        x=[daily_all['createTimeISO'].min(), daily_all['createTimeISO'].max()],
        y=[daily_all['Total'].mean(), daily_all['Total'].mean()],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f'Mean All Day ({mean_all_day.round(2)})',
        visible=True
    ))

    # Last 90 DAYS
    fig_lines.add_trace(go.Scatter(
        x=daily_3month['createTimeISO'],
        y=daily_3month['Total'],
        name='Last 90 Days',
        visible=False
    ))

    fig_lines.add_trace(go.Scatter(
        x=[daily_3month['createTimeISO'].min(), daily_3month['createTimeISO'].max()],
        y=[daily_3month['Total'].mean(), daily_3month['Total'].mean()],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f'Mean 90 Days ({mean_3month.round(2)})',
        visible=False
    ))

    # LAST 30 DAYS
    fig_lines.add_trace(go.Scatter(
        x=daily_month['createTimeISO'],
        y=daily_month['Total'],
        name='Last 30 Days ',
        visible=False
    ))

    fig_lines.add_trace(go.Scatter(
        x=[daily_month['createTimeISO'].min(), daily_month['createTimeISO'].max()],
        y=[daily_month['Total'].mean(), daily_month['Total'].mean()],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f'Mean 30 Days ({mean_month.round(2)})',
        visible=False
    ))

    # LAST 7 DAYS
    fig_lines.add_trace(go.Scatter(
        x=daily_week['createTimeISO'],
        y=daily_week['Total'],
        name='Last 7 Days',
        visible=False
    ))

    fig_lines.add_trace(go.Scatter(
        x=[daily_week['createTimeISO'].min(), daily_week['createTimeISO'].max()],
        y=[daily_week['Total'].mean(), daily_week['Total'].mean()],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f'Mean 7 Days ({mean_week.round(2)})',
        visible=False
    ))

    # LAST 1 DAY (jam)
    fig_lines.add_trace(go.Scatter(
        x=daily_day['createTimeISO'],
        y=daily_day['Total'],
        name='Last 1 Day',
        visible=False
    ))

    fig_lines.add_trace(go.Scatter(
        x=[daily_day['createTimeISO'].min(), daily_day['createTimeISO'].max()],
        y=[daily_day['Total'].mean(), daily_day['Total'].mean()],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f'Mean 1 Day ({mean_day.round(2)})',
        visible=False
    ))

    # DROPDOWN MENU
    fig_lines.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(label="All Time", method="update",
                        args=[{"visible": [True, True, False, False, False, False, False, False, False, False]}]),

                    dict(label="Last 90 Days", method="update",
                        args=[{"visible": [False, False, True, True, False, False, False, False, False, False]}]),

                    dict(label="Last 30 Days", method="update",
                        args=[{"visible": [False, False, False, False, True, True, False, False, False, False]}]),

                    dict(label="Last 7 Days", method="update",
                        args=[{"visible": [False, False, False, False, False, False, True, True, False, False]}]),

                    dict(label="Last 1 Day", method="update",
                        args=[{"visible": [False, False, False, False, False, False, False, False, True, True]}]),
                ],
                x=0.1, y=1.15
            )
        ],
        title={'text': "Video Upload Activity Over Time", 'x': 0.5},
        xaxis_title="Time",
        yaxis_title="Total Videos"
    )

    return fig_lines

def likes_over_time(df):
    """Analisis like video dari waktu ke waktu (Total Likes per periode)."""

    df['createTimeISO'] = pd.to_datetime(df['createTimeISO'])

    # === Tentukan tanggal terakhir ===
    latest_date = df['createTimeISO'].max()

    # === Rentang waktu ===
    three_month = latest_date - pd.Timedelta(days=90)
    one_month  = latest_date - pd.Timedelta(days=30)
    one_week   = latest_date - pd.Timedelta(days=7)
    one_day    = latest_date - pd.Timedelta(days=1)

    # === Filter data ===
    data_all      = df
    data_90d      = df[df['createTimeISO'] >= three_month]
    data_30d      = df[df['createTimeISO'] >= one_month]
    data_7d       = df[df['createTimeISO'] >= one_week]
    data_1d       = df[df['createTimeISO'] >= one_day]

    # Resample Likes
    daily_all  = data_all.resample('D', on='createTimeISO')['diggCount'].sum().reset_index(name='Likes')
    daily_90d  = data_90d.resample('D', on='createTimeISO')['diggCount'].sum().reset_index(name='Likes')
    daily_30d  = data_30d.resample('D', on='createTimeISO')['diggCount'].sum().reset_index(name='Likes')
    daily_7d   = data_7d.resample('D', on='createTimeISO')['diggCount'].sum().reset_index(name='Likes')
    hourly_1d  = data_1d.resample('H', on='createTimeISO')['diggCount'].sum().reset_index(name='Likes')

    # Mean Likes
    mean_all  = daily_all['Likes'].mean()
    mean_90d  = daily_90d['Likes'].mean() if len(daily_90d) else 0
    mean_30d  = daily_30d['Likes'].mean() if len(daily_30d) else 0
    mean_7d   = daily_7d['Likes'].mean() if len(daily_7d) else 0
    mean_1d   = hourly_1d['Likes'].mean() if len(hourly_1d) else 0

    fig_likes_line = go.Figure()

    # ALL TIME
    fig_likes_line.add_trace(go.Scatter(
        x=daily_all['createTimeISO'],
        y=daily_all['Likes'],
        name='All Time Likes',
        visible=True
    ))
    fig_likes_line.add_trace(go.Scatter(
        x=[daily_all['createTimeISO'].min(), daily_all['createTimeISO'].max()],
        y=[mean_all, mean_all],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f"Mean All ({mean_all:.2f})",
        visible=True
    ))

    # LAST 90 DAYS
    fig_likes_line.add_trace(go.Scatter(
        x=daily_90d['createTimeISO'],
        y=daily_90d['Likes'],
        name='Last 90 Days Likes',
        visible=False
    ))
    fig_likes_line.add_trace(go.Scatter(
        x=[daily_90d['createTimeISO'].min(), daily_90d['createTimeISO'].max()] if len(daily_90d) else [None, None],
        y=[mean_90d, mean_90d],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f"Mean 90 Days ({mean_90d:.2f})",
        visible=False
    ))

    # LAST 30 DAYS
    fig_likes_line.add_trace(go.Scatter(
        x=daily_30d['createTimeISO'],
        y=daily_30d['Likes'],
        name='Last 30 Days Likes',
        visible=False
    ))
    fig_likes_line.add_trace(go.Scatter(
        x=[daily_30d['createTimeISO'].min(), daily_30d['createTimeISO'].max()] if len(daily_30d) else [None, None],
        y=[mean_30d, mean_30d],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f"Mean 30 Days ({mean_30d:.2f})",
        visible=False
    ))

    # LAST 7 DAYS
    fig_likes_line.add_trace(go.Scatter(
        x=daily_7d['createTimeISO'],
        y=daily_7d['Likes'],
        name='Last 7 Days Likes',
        visible=False
    ))
    fig_likes_line.add_trace(go.Scatter(
        x=[daily_7d['createTimeISO'].min(), daily_7d['createTimeISO'].max()] if len(daily_7d) else [None, None],
        y=[mean_7d, mean_7d],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f"Mean 7 Days ({mean_7d:.2f})",
        visible=False
    ))

    # LAST 1 DAY (Hourly)
    fig_likes_line.add_trace(go.Scatter(
        x=hourly_1d['createTimeISO'],
        y=hourly_1d['Likes'],
        name='Last 24 Hours Likes',
        visible=False
    ))
    fig_likes_line.add_trace(go.Scatter(
        x=[hourly_1d['createTimeISO'].min(), hourly_1d['createTimeISO'].max()] if len(hourly_1d) else [None, None],
        y=[mean_1d, mean_1d],
        mode='lines',
        line=dict(dash='dash', color='red'),
        name=f"Mean 24 Hours ({mean_1d:.2f})",
        visible=False
    ))

    # DROPDOWN
    fig_likes_line.update_layout(
        updatemenus=[
            dict(
                buttons=[
                    dict(label="All Time", 
                         method="update",
                         args=[{"visible": [True, True,  False, False, False, False, False, False, False, False]}]),

                    dict(label="Last 90 Days", 
                         method="update",
                         args=[{"visible": [False, False, True, True, False, False, False, False, False, False]}]),

                    dict(label="Last 30 Days", 
                         method="update",
                         args=[{"visible": [False, False, False, False, True, True, False, False, False, False]}]),

                    dict(label="Last 7 Days", 
                         method="update",
                         args=[{"visible": [False, False, False, False, False, False, True, True, False, False]}]),

                    dict(label="Last 24 Hours", 
                         method="update",
                         args=[{"visible": [False, False, False, False, False, False, False, False, True, True]}]),
                ],
                x=0.1, y=1.15
            )
        ],
        title={'text': "Likes Over Time", 'x': 0.5},
        xaxis_title="Time",
        yaxis_title="Total Likes"
    )

    return fig_likes_line