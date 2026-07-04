% order5v2_1470  eq1=38088 eq2=54747  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(X,f(f(Y,X),Y)),Y),Z) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,f(X,Y)) = f(X,f(f(Y,X),Y)) )).
