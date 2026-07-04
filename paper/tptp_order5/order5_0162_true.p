% order5_0162  eq1=36871 eq2=47395  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(f(Y,Z),Y),f(Y,Y)),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Z,Y),f(f(Y,Y),Y)) )).
