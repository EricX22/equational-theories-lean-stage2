% order5v2_1556  eq1=275 eq2=59542  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,X),Y),Z) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),Y) = f(Z,f(f(Z,Z),W)) )).
