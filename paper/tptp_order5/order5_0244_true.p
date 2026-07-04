% order5_0244  eq1=10288 eq2=26136  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(X,Z),f(f(W,X),W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(Y,f(f(Y,Y),X)),f(X,Z)) )).
