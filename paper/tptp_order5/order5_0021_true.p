% order5_0021  eq1=48386 eq2=41519  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,f(Z,W)),f(Y,W)) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( X = f(f(f(f(f(Y,Z),W),U),U),W) )).
