% order5_0246  eq1=18442 eq2=13095  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Z),f(Y,f(f(X,Z),Z))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(Z,f(X,f(X,X))),Z)) )).
