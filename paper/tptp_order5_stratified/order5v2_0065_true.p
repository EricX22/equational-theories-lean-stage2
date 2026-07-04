% order5v2_0065  eq1=1294 eq2=59469  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(X,Y),Z),W)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(f(X,Y),Y) = f(Y,f(f(X,Z),W)) )).
