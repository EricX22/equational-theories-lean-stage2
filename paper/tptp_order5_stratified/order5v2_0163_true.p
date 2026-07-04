% order5v2_0163  eq1=2297 eq2=20932  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,f(X,f(X,Z))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,Y),f(f(f(Z,Y),Y),Z)) )).
