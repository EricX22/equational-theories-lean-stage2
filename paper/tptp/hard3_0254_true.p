% hard3_0254  eq1=2364 eq2=3694  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(Z,f(X,X))),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,X) = f(f(Y,Z),f(X,X)) )).
