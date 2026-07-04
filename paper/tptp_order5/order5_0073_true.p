% order5_0073  eq1=12856 eq2=37893  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,f(Y,f(Z,Z))),X)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(Y,f(Z,f(W,X))),Z),W) )).
