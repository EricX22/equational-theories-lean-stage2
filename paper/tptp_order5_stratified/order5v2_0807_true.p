% order5v2_0807  eq1=13065 eq2=19713  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,f(Z,f(Z,W))),W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,Y),f(f(Y,f(Z,X)),X)) )).
