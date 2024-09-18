# lionel_app

A Streamlit App to display the results of the [lionel](https://github.com/jth500/lionel) FPL team picking tool.

## The model

Lionel estimates points using a match and player level model.

For the home team:

$$
\text{N}_{\text{goals scored, home}} \sim \text{Poisson}(\lambda_{\text{home}})
$$

$$
\text{N}_{\text{goals conceded, home}} \sim \text{Poisson}(\lambda_{\text{away}})
$$

where:

$$
\text{log}(\lambda_{\text{home}}) = \beta_0 + \beta_{\text{home advantage}} + \beta_{\text{attack, home team}} + \beta_{\text{defence, away team}}
$$

and $\lambda_{\text{away}}$ has a similar formulation.

Then, at the player level:

$$
\text{Points}_{\text{player, match}} \sim \mathcal{N}(\mu_{\text{player, match}}, \sigma^2 )
$$

where:

$$
\mu_{\text{player, match}} = \text{p}_{\text{goals, position}}\text{n}_{\text{goals}} + \text{p}_{\text{goals, position}}\text{n}_{\text{assists}} + \text{p}_{\text{clean sheet, position}}\gamma_\text{clean sheet} + \alpha_\text{player}
$$

Where:

$$
\text{n}_{\text{goals}}, \text{n}_{\text{assists}}, \text{n}_\text{neither} \sim 
                \text{Multinomial}(\text{N}_\text{goals scored, home}, \text{p}_{\text{score}}, \text{p}_{\text{assist}}, \text{p}_{\text{neither}})
$$

$$
\gamma_\text{clean sheet} = 1 \text{  if  } \text{N}_{\text{goals conceded}}=1
$$

$$
\alpha_{\text{player}} \sim \mathcal{N}(\mu_\text{player}, \sigma_{\alpha}^2)
$$

and $\text{p}_{\text{event, position}}$ denotes the number of points that each position earns for a goal, assist, or clean sheet.

An analogous model is used for players on the away team.