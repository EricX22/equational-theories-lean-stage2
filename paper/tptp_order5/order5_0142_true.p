% order5_0142  eq1=29305 eq2=39585  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(X,f(Y,f(X,f(X,X)))),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(f(f(f(Y,Z),f(Z,Y)),Z),W) )).
