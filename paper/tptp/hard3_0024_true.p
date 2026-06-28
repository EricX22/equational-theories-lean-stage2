% hard3_0024  eq1=112 eq2=2277  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(X,f(f(Y,Z),Z)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,f(Z,Y))),X) )).
