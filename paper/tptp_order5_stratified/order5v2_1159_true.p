% order5v2_1159  eq1=12186 eq2=10852  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),Z),f(W,Y))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(f(X,f(Y,X)),f(Y,X))) )).
