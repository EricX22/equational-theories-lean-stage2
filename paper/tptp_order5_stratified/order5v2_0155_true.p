% order5v2_0155  eq1=20935 eq2=23659  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(Y,Y),f(f(f(Z,Y),Z),Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),X),f(Z,f(Z,X))) )).
