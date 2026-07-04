% order5v2_0478  eq1=16964 eq2=43076  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(f(f(Z,W),U),U),U)) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(Z,f(Z,f(f(X,Z),W))) )).
